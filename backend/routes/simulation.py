"""REST API routes exposing the propagation simulation engine."""

import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List
import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# Ensure src is discoverable
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from propagation.analysis.comparator import ModelComparator
from propagation.core.link_budget import LinkBudget
from propagation.models import (
    FreeSpacePathLoss,
    TwoRayGroundReflection,
    LogDistancePathLoss,
    OkumuraModel,
    HataModel,
    COST231HataModel,
    LogNormalShadowing,
)
from propagation.visualization.plotting import MODEL_LABELS

from backend.schemas import SimulationRequest, LinkBudgetEvaluationRequest

router = APIRouter(prefix="/api", tags=["Simulation"])

MODEL_METADATA = {
    "fspl": {
        "name": "Free Space (Friis)",
        "color": "#0284c7",
        "strokeDash": "0",
        "lineType": "Solid Line (Blue)",
        "formula": "PL = 20·log10(d) + 20·log10(f) + 32.44",
        "shortDesc": "Theoretical vacuum Line-of-Sight lower bound (n = 2.0, 20 dB/decade).",
    },
    "two_ray": {
        "name": "Two-Ray Ground Reflection",
        "color": "#f97316",
        "strokeDash": "6 4",
        "lineType": "Dashed Line (Orange)",
        "formula": "PL = 40·log10(d) − (10·log10(Gt·Gr) + 20·log10(ht·hr))",
        "shortDesc": "Accounts for direct wave + ground bounce reflection interference (40 dB/decade far-field).",
    },
    "log_distance": {
        "name": "Log-Distance",
        "color": "#16a34a",
        "strokeDash": "8 4 2 4",
        "lineType": "Dash-Dot Line (Green)",
        "formula": "PL(d) = PL(d0) + 10·n·log10(d / d0)",
        "shortDesc": "Environment-tunable empirical exponent model capturing macro/indoor attenuation.",
    },
    "okumura": {
        "name": "Okumura Model",
        "color": "#dc2626",
        "strokeDash": "3 3",
        "lineType": "Dotted Line (Red)",
        "formula": "PL = L_FS + A_mu(f,d) − G(ht) − G(hr) − G_area",
        "shortDesc": "Empirical drive-test nomogram measurements calibrated in Tokyo (1968).",
    },
    "hata": {
        "name": "Okumura-Hata",
        "color": "#14532d",
        "strokeDash": "0",
        "lineType": "Solid Bold Line (Forest Green)",
        "formula": "PL = 69.55 + 26.16·log10(f) − 13.82·log10(ht) − a(hr) + [44.9 − 6.55·log10(ht)]·log10(d)",
        "shortDesc": "Standard closed-form cellular macrocell planning formula derived from Okumura.",
    },
    "cost231": {
        "name": "COST-231 Hata",
        "color": "#7c3aed",
        "strokeDash": "6 4",
        "lineType": "Dashed Line (Violet)",
        "formula": "PL = 46.3 + 33.9·log10(f) − 13.82·log10(ht) − a(hr) + [44.9 − 6.55·log10(ht)]·log10(d) + Cm",
        "shortDesc": "Extended Hata formulation supporting 1500–2000 MHz PCS/4G bands.",
    },
    "shadowing": {
        "name": "Log-Normal Shadowing",
        "color": "#db2777",
        "strokeDash": "0",
        "lineType": "Solid Stochastic Line (Magenta)",
        "formula": "PL(d) = PL(d0) + 10·n·log10(d/d0) + Xσ",
        "shortDesc": "Adds zero-mean Gaussian random shadowing (Xσ in dB) for realistic spatial variability.",
    },
}


def _build_models(env: str, ht_m: float, hr_m: float, sigma_db: float) -> Dict[str, Any]:
    return {
        "fspl": FreeSpacePathLoss(),
        "two_ray": TwoRayGroundReflection(ht_default=ht_m, hr_default=hr_m),
        "log_distance": LogDistancePathLoss(
            environment=env if env in ["urban", "suburban", "rural", "indoor_obstructed"] else "urban"
        ),
        "okumura": OkumuraModel(
            hte_default=ht_m,
            hre_default=hr_m,
            environment="open" if env == "rural" else env,
        ),
        "hata": HataModel(
            hb_default=ht_m,
            hm_default=hr_m,
            environment="rural" if env == "rural" else ("suburban" if env == "suburban" else "urban_medium"),
        ),
        "cost231": COST231HataModel(
            hb_default=ht_m,
            hm_default=hr_m,
            environment="suburban" if env == "suburban" else "medium_city",
        ),
        "shadowing": LogNormalShadowing(n=3.0, sigma_db=sigma_db, seed=42),
    }


@router.post("/simulate")
def run_simulation(req: SimulationRequest) -> Dict[str, Any]:
    """Run full multi-model path loss, received power, outage, and stats simulation."""
    min_d = min(req.min_distance_km, req.max_distance_km - 0.05)
    distances_km = np.geomspace(max(0.01, min_d), req.max_distance_km, req.num_points)

    budget = LinkBudget(
        tx_power_dbm=req.tx_power_dbm,
        tx_gain_dbi=req.tx_gain_dbi,
        rx_gain_dbi=req.rx_gain_dbi,
        system_loss_db=req.system_loss_db,
        rx_sensitivity_dbm=req.rx_sensitivity_dbm,
    )

    instances = _build_models(req.environment, req.ht_m, req.hr_m, req.shadow_sigma_db)

    points: List[Dict[str, Any]] = []
    stats: List[Dict[str, Any]] = []

    pl_by_model: Dict[str, np.ndarray] = {}
    pr_by_model: Dict[str, np.ndarray] = {}

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for m_key in req.models:
            if m_key not in instances:
                continue
            model = instances[m_key]
            kwargs: Dict[str, Any] = {}
            if m_key == "two_ray":
                kwargs = {"ht": req.ht_m, "hr": req.hr_m}
            elif m_key in {"okumura", "hata", "cost231"}:
                kwargs = {"hb": req.ht_m, "hm": req.hr_m, "hte": req.ht_m, "hre": req.hr_m}
            elif m_key == "shadowing":
                kwargs = {"seed": 42}

            pl_arr = np.asarray(
                model.calculate_path_loss(
                    distance=distances_km,
                    frequency=req.frequency_mhz,
                    distance_unit="km",
                    frequency_unit="MHz",
                    strict=False,
                    **kwargs,
                ),
                dtype=np.float64,
            )
            pr_arr = np.asarray(budget.calculate_received_power_dbm(pl_arr), dtype=np.float64)

            pl_by_model[m_key] = pl_arr
            pr_by_model[m_key] = pr_arr

            stats.append({
                "key": m_key,
                "model": MODEL_LABELS.get(m_key, m_key),
                "min_pl_db": round(float(np.min(pl_arr)), 2),
                "max_pl_db": round(float(np.max(pl_arr)), 2),
                "mean_pl_db": round(float(np.mean(pl_arr)), 2),
                "std_pl_db": round(float(np.std(pl_arr)), 2),
                "min_pr_dbm": round(float(np.min(pr_arr)), 2),
                "max_pr_dbm": round(float(np.max(pr_arr)), 2),
                "mean_pr_dbm": round(float(np.mean(pr_arr)), 2),
            })

        shadow_model = instances["shadowing"]
        outage_arr = np.asarray(
            shadow_model.calculate_outage_probability(
                distance=distances_km,
                frequency=req.frequency_mhz,
                rx_sensitivity_dbm=req.rx_sensitivity_dbm,
                tx_power_dbm=req.tx_power_dbm,
                tx_gain_dbi=req.tx_gain_dbi,
                rx_gain_dbi=req.rx_gain_dbi,
                system_loss_db=req.system_loss_db,
                distance_unit="km",
                frequency_unit="MHz",
                sigma=req.shadow_sigma_db,
            )
            * 100.0,
            dtype=np.float64,
        )

    for idx in range(len(distances_km)):
        row: Dict[str, Any] = {
            "distance_km": round(float(distances_km[idx]), 3),
            "outage_pct": round(float(outage_arr[idx]), 2),
            "rx_sensitivity_dbm": float(req.rx_sensitivity_dbm),
        }
        for m_key in pl_by_model:
            row[f"pl_{m_key}"] = round(float(pl_by_model[m_key][idx]), 2)
            row[f"pr_{m_key}"] = round(float(pr_by_model[m_key][idx]), 2)
        points.append(row)

    # Midpoint KPI summary
    mid_idx = len(distances_km) // 2
    mid_d = round(float(distances_km[mid_idx]), 2)
    fspl_mid = round(float(pl_by_model["fspl"][mid_idx]), 2) if "fspl" in pl_by_model else None
    hata_mid = round(float(pl_by_model["hata"][mid_idx]), 2) if "hata" in pl_by_model else None

    return {
        "eirp_dbm": round(float(budget.eirp_dbm), 2),
        "mid_distance_km": mid_d,
        "fspl_mid_db": fspl_mid,
        "hata_mid_db": hata_mid,
        "points": points,
        "stats": stats,
        "model_metadata": {k: MODEL_METADATA[k] for k in req.models if k in MODEL_METADATA},
    }


@router.get("/comparison-matrix")
def get_comparison_matrix() -> Dict[str, Any]:
    """Return the formal academic comparison matrix for all 7 models."""
    df = ModelComparator.get_comparison_table()
    return {
        "columns": list(df.columns),
        "rows": df.to_dict(orient="records"),
    }


@router.get("/benchmark-900mhz")
def get_benchmark_900mhz() -> Dict[str, Any]:
    """Return the exact 21CSE458T mini-project 900 MHz course benchmark table (1–20 km)."""
    d = np.arange(1, 21, dtype=np.float64)
    f = 900.0
    ht = 30.0
    hr = 1.5

    fspl = 20.0 * np.log10(d) + 20.0 * np.log10(f) + 32.44
    a_hre = (1.1 * np.log10(f) - 0.7) * hr - (1.56 * np.log10(f) - 0.8)
    hata = 69.55 + 26.16 * np.log10(f) - 13.82 * np.log10(ht) - a_hre + (44.9 - 6.55 * np.log10(ht)) * np.log10(d)
    corr = -4.78 * (np.log10(f) ** 2) + 18.33 * np.log10(f) - 40.94
    okumura = hata + corr

    rows = []
    for i in range(len(d)):
        rows.append({
            "distance_km": int(d[i]),
            "fspl_db": round(float(fspl[i]), 2),
            "okumura_db": round(float(okumura[i]), 2),
            "hata_urban_db": round(float(hata[i]), 2),
            "delta_hata_fspl_db": round(float(hata[i] - fspl[i]), 2),
        })
    return {
        "parameters": {"frequency_mhz": f, "ht_m": ht, "hr_m": hr},
        "rows": rows,
    }


@router.post("/link-budget")
def evaluate_link_budget(req: LinkBudgetEvaluationRequest) -> Dict[str, Any]:
    """Compute exact RF link budget chain at a single target distance."""
    budget = LinkBudget(
        tx_power_dbm=req.tx_power_dbm,
        tx_gain_dbi=req.tx_gain_dbi,
        rx_gain_dbi=req.rx_gain_dbi,
        system_loss_db=req.system_loss_db,
        rx_sensitivity_dbm=req.rx_sensitivity_dbm,
    )
    instances = _build_models(req.environment, req.ht_m, req.hr_m, 6.0)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fspl_pl = float(
            instances["fspl"].calculate_path_loss(
                distance=req.target_distance_km, frequency=req.frequency_mhz, distance_unit="km", frequency_unit="MHz", strict=False
            )
        )
        cellular_model_key = "cost231" if req.frequency_mhz > 1500 else "hata"
        cellular_pl = float(
            instances[cellular_model_key].calculate_path_loss(
                distance=req.target_distance_km,
                frequency=req.frequency_mhz,
                distance_unit="km",
                frequency_unit="MHz",
                strict=False,
                hb=req.ht_m,
                hm=req.hr_m,
            )
        )

    rx_power_dbm = float(budget.calculate_received_power_dbm(cellular_pl))
    fade_margin_db = float(budget.calculate_fade_margin(cellular_pl))

    return {
        "target_distance_km": req.target_distance_km,
        "cellular_model_used": MODEL_LABELS[cellular_model_key],
        "eirp_dbm": round(float(budget.eirp_dbm), 2),
        "fspl_loss_db": round(fspl_pl, 2),
        "cellular_loss_db": round(cellular_pl, 2),
        "rx_power_dbm": round(rx_power_dbm, 2),
        "fade_margin_db": round(fade_margin_db, 2),
        "link_status": "SERVICE OK" if fade_margin_db > 0 else "OUTAGE RISK",
    }


@router.get("/download-case-study")
def download_case_study():
    """Serve the generated Case_Study_Document.docx file for direct browser download."""
    doc_path = ROOT_DIR / "Case_Study_Document.docx"
    if not doc_path.exists():
        raise HTTPException(status_code=404, detail="Case Study document not found")
    return FileResponse(
        path=str(doc_path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="Wireless_Propagation_Case_Study.docx",
    )


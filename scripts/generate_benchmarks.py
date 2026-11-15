"""
Multi-Frequency & Multi-Distance Benchmark Table Generator.

Evaluates Classical, 3GPP TR 38.901, CI, ABG, and LoS-NLoS Transition models across:
  Frequencies: 1.8 GHz, 3.5 GHz, 13 GHz, 28 GHz
  Distances:
    - Micro / mmWave: 50 m, 100 m, 200 m
    - Macro: 1 km, 5 km, 10 km
Exports to outputs/reports/benchmark_summary_table.csv.
"""

from pathlib import Path
import warnings
import numpy as np
import pandas as pd

from propagation.core.exceptions import ModelRangeWarning
from propagation.models.free_space import FreeSpacePathLoss
from propagation.models.two_ray import TwoRayGroundReflection
from propagation.models.log_distance import LogDistancePathLoss
from propagation.models.okumura import OkumuraModel
from propagation.models.hata import HataModel
from propagation.models.cost231 import COST231HataModel
from propagation.models.shadowing import LogNormalShadowing
from propagation.models.three_gpp_tr38901 import ThreeGPPUMiModel, ThreeGPPUMaModel
from propagation.models.ci_abg import CloseInModel, FloatingInterceptABGModel
from propagation.models.los_nlos_transition import StatisticalLoSNLoSTransitionModel

ROOT_DIR = Path(__file__).resolve().parent.parent


def evaluate_model_safe(model_func, d_m: float, f_hz: float, valid_d: tuple, valid_f: tuple) -> str:
    """Evaluate path loss in dB or report range limitation."""
    is_f_valid = valid_f[0] <= f_hz <= valid_f[1]
    is_d_valid = valid_d[0] <= d_m <= valid_d[1]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ModelRangeWarning)
        try:
            val = float(model_func(d_m, f_hz))
            if not is_f_valid or not is_d_valid:
                reasons = []
                if not is_f_valid:
                    reasons.append(f"f outside [{valid_f[0]/1e9:.2f}, {valid_f[1]/1e9:.2f}] GHz")
                if not is_d_valid:
                    reasons.append(f"d outside [{valid_d[0]:.0f}, {valid_d[1]:.0f}] m")
                return f"{val:.1f}* (OOR: {'; '.join(reasons)})"
            return f"{val:.1f}"
        except Exception:
            return "N/A"


def generate_benchmark_table() -> pd.DataFrame:
    frequencies = [
        ("1.8 GHz", 1.8e9),
        ("3.5 GHz", 3.5e9),
        ("13 GHz", 13.0e9),
        ("28 GHz", 28.0e9),
    ]

    distances = [
        ("50 m", 50.0),
        ("100 m", 100.0),
        ("200 m", 200.0),
        ("1 km", 1000.0),
        ("5 km", 5000.0),
        ("10 km", 10000.0),
    ]

    # Instantiate models
    fspl = FreeSpacePathLoss()
    two_ray = TwoRayGroundReflection(ht_default=25.0, hr_default=1.5)
    log_dist = LogDistancePathLoss(n=3.0, d0_m=1.0)
    okumura = OkumuraModel(hte_default=25.0, hre_default=1.5)
    hata = HataModel(hb_default=25.0, hm_default=1.5)
    cost231 = COST231HataModel(hb_default=25.0, hm_default=1.5)
    shadowing = LogNormalShadowing(n=3.0, sigma_db=6.0, d0_m=1.0, seed=42)

    umi_los = ThreeGPPUMiModel(mode="los", hbs_default=10.0, hut_default=1.5)
    umi_nlos = ThreeGPPUMiModel(mode="nlos", hbs_default=10.0, hut_default=1.5)
    uma_los = ThreeGPPUMaModel(mode="los", hbs_default=25.0, hut_default=1.5)
    uma_nlos = ThreeGPPUMaModel(mode="nlos", hbs_default=25.0, hut_default=1.5)
    ci_nlos = CloseInModel(n=3.19, sigma_db=8.2)
    abg = FloatingInterceptABGModel()
    transition = StatisticalLoSNLoSTransitionModel(hbs_default=10.0, hut_default=1.5, seed=42)

    model_definitions = [
        ("Free Space (Friis)", lambda d, f: fspl.calculate_path_loss(d, f, "m", "Hz"), (1.0, 100000.0), (1e6, 100e9)),
        ("Two-Ray Ground Reflection", lambda d, f: two_ray.calculate_path_loss(d, f, "m", "Hz"), (1.0, 100000.0), (1e6, 60e9)),
        ("Log-Distance (n=3.0)", lambda d, f: log_dist.calculate_path_loss(d, f, "m", "Hz"), (1.0, 100000.0), (10e6, 60e9)),
        ("Okumura Model", lambda d, f: okumura.calculate_path_loss(d/1000.0, f/1e6, "km", "MHz", environment="urban"), (1000.0, 100000.0), (150e6, 1920e6)),
        ("Okumura-Hata Model", lambda d, f: hata.calculate_path_loss(d/1000.0, f/1e6, "km", "MHz", environment="urban_large"), (1000.0, 20000.0), (150e6, 1500e6)),
        ("COST-231 Hata Model", lambda d, f: cost231.calculate_path_loss(d/1000.0, f/1e6, "km", "MHz", environment="urban_medium"), (1000.0, 20000.0), (1500e6, 2000e6)),
        ("Log-Normal Shadowing (Median)", lambda d, f: shadowing.calculate_path_loss(d, f, "m", "Hz", include_shadowing=False), (1.0, 100000.0), (10e6, 100e9)),
        ("3GPP TR 38.901 UMi LoS", lambda d, f: umi_los.calculate_path_loss(d, f, "m", "Hz", los=True), (10.0, 5000.0), (0.5e9, 100e9)),
        ("3GPP TR 38.901 UMi NLoS", lambda d, f: umi_nlos.calculate_path_loss(d, f, "m", "Hz", los=False), (10.0, 5000.0), (0.5e9, 100e9)),
        ("3GPP TR 38.901 UMa LoS", lambda d, f: uma_los.calculate_path_loss(d, f, "m", "Hz", los=True), (10.0, 10000.0), (0.5e9, 100e9)),
        ("3GPP TR 38.901 UMa NLoS", lambda d, f: uma_nlos.calculate_path_loss(d, f, "m", "Hz", los=False), (10.0, 5000.0), (0.5e9, 100e9)),
        ("Close-In (CI) Model (n=3.19)", lambda d, f: ci_nlos.calculate_path_loss(d, f, "m", "Hz", los=False), (1.0, 5000.0), (0.5e9, 100e9)),
        ("Floating-Intercept (ABG)", lambda d, f: abg.calculate_path_loss(d, f, "m", "Hz"), (1.0, 5000.0), (0.5e9, 100e9)),
        ("LoS-NLoS Transition Mean", lambda d, f: transition.calculate_path_loss(d, f, "m", "Hz", mode="expectation"), (10.0, 5000.0), (0.5e9, 100e9)),
    ]

    records = []
    for model_name, func, d_bounds, f_bounds in model_definitions:
        for f_label, f_hz in frequencies:
            row = {
                "Model": model_name,
                "Frequency": f_label,
            }
            for d_label, d_m in distances:
                row[d_label] = evaluate_model_safe(func, d_m, f_hz, d_bounds, f_bounds)
            records.append(row)

    df = pd.DataFrame(records)
    return df


def main():
    print("Generating comprehensive multi-frequency benchmark table...")
    df = generate_benchmark_table()
    out_dir = ROOT_DIR / "outputs" / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "benchmark_summary_table.csv"
    df.to_csv(csv_path, index=False)
    print(f"[+] Benchmark summary table saved to: {csv_path}")
    print("\nSample Preview (28 GHz mmWave):")
    preview = df[df["Frequency"] == "28 GHz"][["Model", "Frequency", "50 m", "100 m", "200 m", "1 km"]]
    print(preview.to_string(index=False))


if __name__ == "__main__":
    main()

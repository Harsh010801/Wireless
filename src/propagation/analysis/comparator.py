"""
Comparative analysis engine: model differences, statistical metrics, and comparison matrix.
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from propagation.simulation.engine import SimulationResult


# Canonical formal taxonomy and reference matrix for propagation models
FORMAL_MODEL_COMPARISON: List[Dict[str, str]] = [
    {
        "Model": "Free Space (Friis)",
        "Classification": "Theoretical (Deterministic)",
        "Complexity": "O(1) Closed-form",
        "Environment": "Unobstructed LOS / Space / Anechoic",
        "Frequency Range": "Broadband (All frequencies)",
        "Distance Range": "Far-field (d > 2D^2 / lambda)",
        "Main Advantage": "Exact Maxwell-derived baseline with zero empirical tuning parameters",
        "Main Limitation": "Severely underestimates loss in terrestrial multipath & cluttered terrain",
    },
    {
        "Model": "Two-Ray Ground Reflection",
        "Classification": "Theoretical (Multipath)",
        "Complexity": "O(1) Geometric Vector",
        "Environment": "Flat earth, rural, highways, waterways",
        "Frequency Range": "VHF to mmWave (1 MHz - 60 GHz)",
        "Distance Range": "1 m - 100 km (Asymptotic d > d_c)",
        "Main Advantage": "Captures destructive ground reflection and asymptotic d^-4 power roll-off",
        "Main Limitation": "Unrealistic in dense urban canyons with irregular clutter & 3D scattering",
    },
    {
        "Model": "Log-Distance Path Loss",
        "Classification": "Empirical (Parametric)",
        "Complexity": "O(1) Logarithmic Fit",
        "Environment": "Indoor, microcell, configurable",
        "Frequency Range": "Bespoke to calibration data",
        "Distance Range": "d >= d_0 (Indoor: 1 m, Outdoor: 100 m)",
        "Main Advantage": "Flexible exponent n adaptable to any calibrated environment",
        "Main Limitation": "Requires empirical measurement data to select accurate exponent n",
    },
    {
        "Model": "Okumura Model",
        "Classification": "Empirical (Graphical)",
        "Complexity": "O(1) Empirical Curve Fit",
        "Environment": "Urban, suburban, open macrocells",
        "Frequency Range": "150 MHz - 1920 MHz",
        "Distance Range": "1 km - 100 km",
        "Main Advantage": "Vast field validation under diverse Japanese terrain conditions",
        "Main Limitation": "Extrapolations below 1 km or outside 150-1920 MHz are uncalibrated",
    },
    {
        "Model": "Okumura-Hata Model",
        "Classification": "Empirical (Parametric)",
        "Complexity": "O(1) Closed-form Analytical",
        "Environment": "Urban, suburban, open/rural macrocells",
        "Frequency Range": "150 MHz - 1500 MHz",
        "Distance Range": "1 km - 20 km",
        "Main Advantage": "Analytical closed-form widely adopted in 2G/3G cellular network design",
        "Main Limitation": "Strict 1.5 GHz ceiling; cannot model microcells with d < 1 km or low hb",
    },
    {
        "Model": "COST-231 Hata",
        "Classification": "Empirical (Extended Hata)",
        "Complexity": "O(1) Closed-form Analytical",
        "Environment": "Urban medium & metropolitan centers",
        "Frequency Range": "1500 MHz - 2000 MHz",
        "Distance Range": "1 km - 20 km",
        "Main Advantage": "Extends Hata into PCS/3G 1.8-2.0 GHz bands with metropolitan correction CM",
        "Main Limitation": "Cannot be directly extrapolated to 5G sub-6 GHz (> 2 GHz) or mmWave",
    },
    {
        "Model": "Log-Normal Shadowing",
        "Classification": "Stochastic (Large-scale fading)",
        "Complexity": "O(N) Monte Carlo / Analytical Q",
        "Environment": "Cluttered urban, suburban, indoor",
        "Frequency Range": "Channel-dependent",
        "Distance Range": "d >= d_0",
        "Main Advantage": "Models realistic spatial clutter variation and enables outage probability computation",
        "Main Limitation": "Stochastic: requires statistical confidence intervals rather than deterministic point values",
    },
]


class ModelComparator:
    """
    Analyzes divergence, differences, and statistical metrics across models.
    """

    @staticmethod
    def get_comparison_table() -> pd.DataFrame:
        """Return the formal comparative analysis matrix as a DataFrame."""
        return pd.DataFrame(FORMAL_MODEL_COMPARISON)

    @staticmethod
    def calculate_pairwise_differences(
        sim_result: SimulationResult, baseline_model: str = "fspl"
    ) -> pd.DataFrame:
        """
        Calculate pointwise path loss difference:
            Delta PL = PL_model - PL_baseline
        """
        if baseline_model not in sim_result.path_loss_db:
            available = list(sim_result.path_loss_db.keys())
            raise ValueError(f"Baseline model '{baseline_model}' not found in simulation result. Available: {available}")

        sweep_col = f"{sim_result.sweep_type}_{sim_result.sweep_unit}"
        baseline_pl = sim_result.path_loss_db[baseline_model]

        diff_dict: Dict[str, np.ndarray] = {sweep_col: sim_result.sweep_values}

        for model_key, pl_arr in sim_result.path_loss_db.items():
            if model_key == baseline_model:
                continue
            diff_dict[f"Delta_PL_{model_key}_vs_{baseline_model}_dB"] = pl_arr - baseline_pl

        return pd.DataFrame(diff_dict)

    @staticmethod
    def calculate_summary_statistics(sim_result: SimulationResult) -> pd.DataFrame:
        """
        Compute descriptive summary statistics (min, max, mean, std, median)
        for each model's predicted path loss and received power.
        """
        records = []
        for model_key in sim_result.path_loss_db.keys():
            pl = sim_result.path_loss_db[model_key]
            pr = sim_result.received_power_dbm[model_key]

            records.append({
                "Model": model_key,
                "Min Path Loss (dB)": float(np.min(pl)),
                "Max Path Loss (dB)": float(np.max(pl)),
                "Mean Path Loss (dB)": float(np.mean(pl)),
                "Std Path Loss (dB)": float(np.std(pl)),
                "Median Path Loss (dB)": float(np.median(pl)),
                "Min Rx Power (dBm)": float(np.min(pr)),
                "Max Rx Power (dBm)": float(np.max(pr)),
                "Mean Rx Power (dBm)": float(np.mean(pr)),
            })
        return pd.DataFrame(records)


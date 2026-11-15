"""
Scientific plotting and publication-quality figure generation.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from propagation.analysis.comparator import ModelComparator
from propagation.analysis.sensitivity import SensitivityAnalyzer
from propagation.models.free_space import FreeSpacePathLoss
from propagation.models.two_ray import TwoRayGroundReflection
from propagation.models.log_distance import LogDistancePathLoss
from propagation.models.hata import HataModel
from propagation.models.cost231 import COST231HataModel
from propagation.models.shadowing import LogNormalShadowing
from propagation.models.three_gpp_tr38901 import ThreeGPPUMiModel, ThreeGPPUMaModel, ThreeGPPInHOfficeModel
from propagation.models.ci_abg import CloseInModel, FloatingInterceptABGModel
from propagation.models.los_nlos_transition import StatisticalLoSNLoSTransitionModel
from propagation.simulation.engine import SimulationEngine, SimulationResult
from propagation.simulation.scenario import ScenarioConfig


# Scientific color palette for consistency across plots
MODEL_PALETTE = {
    "fspl": "#1f77b4",          # Steel Blue
    "two_ray": "#ff7f0e",       # Vivid Orange
    "log_distance": "#2ca02c",  # Green
    "okumura": "#d62728",       # Crimson Red
    "hata": "#9467bd",          # Purple
    "cost231": "#8c564b",       # Brown
    "shadowing": "#e377c2",     # Pink/Magenta
    "three_gpp_umi_los": "#06b6d4",   # Cyan
    "three_gpp_umi_nlos": "#e11d48",  # Rose
    "three_gpp_uma_los": "#0284c7",   # Sky Blue
    "three_gpp_uma_nlos": "#b91c1c",  # Dark Red
    "three_gpp_inh_los": "#10b981",   # Emerald
    "three_gpp_inh_nlos": "#d97706",  # Amber Dark
    "ci": "#ca8a04",                  # Amber
    "cif": "#eab308",                 # Yellow Gold
    "abg": "#4f46e5",                 # Indigo
    "los_nlos_trans": "#84cc16",      # Lime Green
    "mmwave_umi_los": "#06b6d4",     # Cyan
    "mmwave_umi_nlos": "#e11d48",    # Rose
    "mmwave_transition": "#84cc16",  # Lime Green
    "mmwave_ci": "#ca8a04",          # Amber
}

MODEL_LABELS = {
    "fspl": "Free Space (Friis)",
    "two_ray": "Two-Ray Ground Refl.",
    "log_distance": "Log-Distance",
    "okumura": "Okumura Model",
    "hata": "Okumura-Hata",
    "cost231": "COST-231 Hata",
    "shadowing": "Log-Normal Shadowing",
    "three_gpp_umi_los": "3GPP UMi LoS",
    "three_gpp_umi_nlos": "3GPP UMi NLoS",
    "three_gpp_uma_los": "3GPP UMa LoS",
    "three_gpp_uma_nlos": "3GPP UMa NLoS",
    "three_gpp_inh_los": "3GPP InH LoS",
    "three_gpp_inh_nlos": "3GPP InH NLoS",
    "ci": "Close-In (CI) Model",
    "cif": "Close-In Freq-Dep (CIF)",
    "abg": "Floating-Intercept (ABG)",
    "los_nlos_trans": "LoS-NLoS Transition (IEEE Access)",
    "mmwave_umi_los": "3GPP UMi LoS (mmWave)",
    "mmwave_umi_nlos": "3GPP UMi NLoS (mmWave)",
    "mmwave_transition": "LoS-NLoS Transition (IEEE Access)",
    "mmwave_ci": "Close-In (CI) mmWave",
}

MODEL_STYLES = {
    "fspl": "-",
    "two_ray": "--",
    "log_distance": "-.",
    "okumura": ":",
    "hata": "-",
    "cost231": "--",
    "shadowing": "-",
    "three_gpp_umi_los": "-",
    "three_gpp_umi_nlos": "--",
    "three_gpp_uma_los": "-",
    "three_gpp_uma_nlos": "--",
    "three_gpp_inh_los": "-",
    "three_gpp_inh_nlos": "--",
    "ci": ":",
    "cif": "-.",
    "abg": "-.",
    "los_nlos_trans": "-",
    "mmwave_umi_los": "-",
    "mmwave_umi_nlos": "--",
    "mmwave_transition": "-.",
    "mmwave_ci": ":",
}


def setup_matplotlib_style():
    """Apply clean, academic IEEE/ACM journal publication styling."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "grid.alpha": 0.5,
        "grid.linestyle": ":",
    })


class Visualizer:
    """
    Publication-grade plotting manager for wireless propagation simulations.
    """

    def __init__(self, output_dir: Union[str, Path] = "outputs/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        setup_matplotlib_style()

    # 1. Path Loss vs Distance
    def plot_path_loss_vs_distance(
        self, sim_result: SimulationResult, filename: str = "fig01_path_loss_vs_distance.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(8.5, 5.5))
        d_vals = sim_result.sweep_values

        for key, pl in sim_result.path_loss_db.items():
            label = MODEL_LABELS.get(key, key)
            color = MODEL_PALETTE.get(key, None)
            style = MODEL_STYLES.get(key, "-")
            ax.plot(d_vals, pl, label=label, color=color, linestyle=style, linewidth=2.0)

        ax.set_title(f"Path Loss vs Distance — {sim_result.scenario_name}")
        ax.set_xlabel(f"Distance ({sim_result.sweep_unit})")
        ax.set_ylabel("Path Loss (dB)")
        ax.set_xscale("log")
        ax.set_ylim(bottom=max(0, np.min([np.min(v) for v in sim_result.path_loss_db.values()]) - 5))
        ax.grid(True, which="both", ls=":")
        ax.legend(loc="upper left", frameon=True)

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 2. Received Power vs Distance
    def plot_received_power_vs_distance(
        self, sim_result: SimulationResult, filename: str = "fig02_received_power_vs_distance.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(8.5, 5.5))
        d_vals = sim_result.sweep_values

        for key, pr in sim_result.received_power_dbm.items():
            label = MODEL_LABELS.get(key, key)
            color = MODEL_PALETTE.get(key, None)
            style = MODEL_STYLES.get(key, "-")
            ax.plot(d_vals, pr, label=label, color=color, linestyle=style, linewidth=2.0)

        # Mark receiver sensitivity threshold if available
        sens = sim_result.link_budget.get("rx_sensitivity_dbm")
        if sens is not None:
            ax.axhline(sens, color="black", linestyle="--", linewidth=1.5, label=f"Rx Sensitivity ({sens:.0f} dBm)")

        ax.set_title(f"Received Power vs Distance — {sim_result.scenario_name}")
        ax.set_xlabel(f"Distance ({sim_result.sweep_unit})")
        ax.set_ylabel("Received Power (dBm)")
        ax.set_xscale("log")
        ax.grid(True, which="both", ls=":")
        ax.legend(loc="lower left", frameon=True)

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 3. Path Loss vs Frequency
    def plot_path_loss_vs_frequency(
        self, freq_result: SimulationResult, filename: str = "fig03_path_loss_vs_frequency.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(8.5, 5.5))
        f_vals = freq_result.sweep_values

        for key, pl in freq_result.path_loss_db.items():
            label = MODEL_LABELS.get(key, key)
            color = MODEL_PALETTE.get(key, None)
            style = MODEL_STYLES.get(key, "-")
            ax.plot(f_vals, pl, label=label, color=color, linestyle=style, linewidth=2.0)

        ax.set_title(f"Frequency Sensitivity Analysis (Fixed Distance = {freq_result.fixed_parameter_value} {freq_result.fixed_parameter_unit})")
        ax.set_xlabel(f"Carrier Frequency ({freq_result.sweep_unit})")
        ax.set_ylabel("Path Loss (dB)")
        ax.grid(True, ls=":")
        ax.legend(loc="lower right", frameon=True)

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 4. Environmental Comparison
    def plot_environmental_comparison(
        self, filename: str = "fig04_environmental_comparison.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(8.5, 5.5))
        d_km = np.linspace(1.0, 20.0, 150)
        f_mhz = 900.0

        model = HataModel(hb_default=30.0, hm_default=1.5)

        pl_urb_large = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="urban_large")
        pl_urb_med = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="urban_medium")
        pl_sub = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="suburban")
        pl_rur = model.calculate_path_loss(d_km, f_mhz, distance_unit="km", frequency_unit="MHz", environment="rural")

        ax.plot(d_km, pl_urb_large, label="Urban (Large City)", color="#b30000", lw=2.2)
        ax.plot(d_km, pl_urb_med, label="Urban (Medium City)", color="#e65c00", lw=2.0)
        ax.plot(d_km, pl_sub, label="Suburban", color="#2ca02c", lw=2.0, ls="--")
        ax.plot(d_km, pl_rur, label="Rural / Open Area", color="#1f77b4", lw=2.0, ls="-.")

        ax.set_title("Environmental Attenuation Comparison (Hata Model, f = 900 MHz)")
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Path Loss (dB)")
        ax.grid(True, ls=":")
        ax.legend(loc="lower right", frameon=True)

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 5. Model Difference Plot
    def plot_model_difference(
        self, sim_result: SimulationResult, baseline_key: str = "fspl", filename: str = "fig05_model_difference_vs_baseline.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(8.5, 5.5))
        d_vals = sim_result.sweep_values
        baseline_pl = sim_result.path_loss_db[baseline_key]

        for key, pl in sim_result.path_loss_db.items():
            if key == baseline_key:
                continue
            delta = pl - baseline_pl
            label = f"{MODEL_LABELS.get(key, key)} vs Free Space"
            color = MODEL_PALETTE.get(key, None)
            style = MODEL_STYLES.get(key, "-")
            ax.plot(d_vals, delta, label=label, color=color, linestyle=style, lw=2.0)

        ax.axhline(0, color="black", linestyle="--", alpha=0.7)
        ax.set_title(f"Model Path Loss Discrepancy Relative to Free Space ({sim_result.scenario_name})")
        ax.set_xlabel(f"Distance ({sim_result.sweep_unit})")
        ax.set_ylabel("Discrepancy: Delta PL = PL_model - PL_FSPL (dB)")
        ax.set_xscale("log")
        ax.grid(True, which="both", ls=":")
        ax.legend(loc="upper left", frameon=True)

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 6. Shadowing Distribution & Realizations
    def plot_shadowing_analysis(
        self, filename: str = "fig06_shadowing_distribution.png"
    ) -> Path:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
        d_m = np.linspace(10.0, 1000.0, 100)
        f_mhz = 1800.0

        shadow_model = LogNormalShadowing(n=3.0, sigma_db=6.0, d0_m=1.0, seed=42)
        mean_pl, lower_95, upper_95 = shadow_model.calculate_bounds(d_m, f_mhz, confidence=0.95, distance_unit="m", frequency_unit="MHz")

        # Monte Carlo realizations
        realizations = shadow_model.generate_realizations(d_m, f_mhz, num_realizations=8, distance_unit="m", frequency_unit="MHz", seed=42)

        for i in range(len(realizations)):
            ax1.plot(d_m, realizations[i], color="gray", alpha=0.35, lw=1.0)

        ax1.plot(d_m, mean_pl, color="#1f77b4", lw=2.5, label="Deterministic Mean (n=3.0)")
        ax1.fill_between(d_m, lower_95, upper_95, color="#1f77b4", alpha=0.15, label="95% Confidence Interval (+/- 1.96 sigma)")

        ax1.set_title("Log-Normal Shadowing Realizations (sigma = 6 dB)")
        ax1.set_xlabel("Distance (m)")
        ax1.set_ylabel("Path Loss (dB)")
        ax1.grid(True, ls=":")
        ax1.legend(loc="upper left")

        # Histogram at fixed distance d = 500 m
        many_samples = shadow_model.generate_realizations(500.0, f_mhz, num_realizations=1500, distance_unit="m", frequency_unit="MHz", seed=100)
        samples_500 = many_samples[:, 0]

        sns.histplot(samples_500, kde=True, ax=ax2, color="#9467bd", stat="density", bins=30)
        ax2.axvline(np.mean(samples_500), color="red", linestyle="--", label=f"Mean = {np.mean(samples_500):.1f} dB")
        ax2.axvline(np.mean(samples_500) - 1.96*6, color="black", linestyle=":", label="95% Bounds")
        ax2.axvline(np.mean(samples_500) + 1.96*6, color="black", linestyle=":")

        ax2.set_title("Shadow Fading PDF at d = 500 m (1,500 Monte Carlo Runs)")
        ax2.set_xlabel("Path Loss (dB)")
        ax2.set_ylabel("Probability Density")
        ax2.legend(loc="upper right")

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 7. Antenna Height Sensitivity
    def plot_antenna_height_sensitivity(
        self, filename: str = "fig07_antenna_height_sensitivity.png"
    ) -> Path:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

        df_tx = SensitivityAnalyzer.sweep_tx_antenna_height(
            min_ht_m=20.0, max_ht_m=200.0, num_points=60, distance_km=5.0, frequency_mhz=900.0
        )
        ax1.plot(df_tx["tx_height_m"], df_tx["PL_TwoRay_dB"], label="Two-Ray Ground Refl.", color=MODEL_PALETTE["two_ray"], lw=2.0)
        ax1.plot(df_tx["tx_height_m"], df_tx["PL_Okumura_dB"], label="Okumura", color=MODEL_PALETTE["okumura"], lw=2.0, ls=":")
        ax1.plot(df_tx["tx_height_m"], df_tx["PL_Hata_dB"], label="Okumura-Hata", color=MODEL_PALETTE["hata"], lw=2.0, ls="--")
        ax1.set_title("Base Station Antenna Height Sensitivity (d = 5 km, f = 900 MHz)")
        ax1.set_xlabel("Base Station Height ht (m)")
        ax1.set_ylabel("Path Loss (dB)")
        ax1.grid(True, ls=":")
        ax1.legend()

        df_rx = SensitivityAnalyzer.sweep_rx_antenna_height(
            min_hm_m=1.0, max_hm_m=10.0, num_points=50, distance_km=5.0, frequency_mhz=900.0
        )
        ax2.plot(df_rx["rx_height_m"], df_rx["PL_TwoRay_dB"], label="Two-Ray Ground Refl.", color=MODEL_PALETTE["two_ray"], lw=2.0)
        ax2.plot(df_rx["rx_height_m"], df_rx["PL_Okumura_dB"], label="Okumura", color=MODEL_PALETTE["okumura"], lw=2.0, ls=":")
        ax2.plot(df_rx["rx_height_m"], df_rx["PL_Hata_dB"], label="Okumura-Hata", color=MODEL_PALETTE["hata"], lw=2.0, ls="--")
        ax2.set_title("Mobile Antenna Height Sensitivity (d = 5 km, f = 900 MHz)")
        ax2.set_xlabel("Mobile Height hm (m)")
        ax2.set_ylabel("Path Loss (dB)")
        ax2.grid(True, ls=":")
        ax2.legend()

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 8. 2D Path Loss Heatmap
    def plot_path_loss_2d_heatmap(
        self, filename: str = "fig08_path_loss_2d_heatmap.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(8.5, 6.0))
        d_vals = np.linspace(1.0, 15.0, 60)
        f_vals = np.linspace(1500.0, 2000.0, 60)

        D, F, PL = SensitivityAnalyzer.generate_2d_heatmap_grid(
            model_name="cost231", distances_km=d_vals, frequencies_mhz=f_vals
        )

        contour = ax.contourf(D, F, PL, levels=30, cmap="viridis")
        cbar = fig.colorbar(contour, ax=ax)
        cbar.set_label("Path Loss (dB)")

        # Contour lines with numerical labels
        lines = ax.contour(D, F, PL, levels=10, colors="white", alpha=0.5, linewidths=0.8)
        ax.clabel(lines, inline=True, fontsize=8, fmt="%1.0f dB")

        ax.set_title("COST-231 Hata Path Loss Heatmap (Distance vs Frequency)")
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Carrier Frequency (MHz)")

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 9. Model Applicability / Calibration Range Map
    def plot_model_applicability_matrix(
        self, filename: str = "fig09_model_applicability_matrix.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(11.5, 7.5))

        # Model frequency intervals (MHz)
        ranges = [
            ("Free Space (Friis)", 1.0, 100000.0, "Broadband LOS baseline", "#1f77b4"),
            ("Two-Ray Ground Refl.", 1.0, 60000.0, "Multipath Flat Earth", "#ff7f0e"),
            ("Log-Distance", 10.0, 60000.0, "Parametric Indoor/Outdoor", "#2ca02c"),
            ("Okumura Model", 150.0, 1920.0, "Empirical Macro (Tokyo)", "#d62728"),
            ("Okumura-Hata", 150.0, 1500.0, "Empirical Macrocell 2G/3G", "#9467bd"),
            ("COST-231 Hata", 1500.0, 2000.0, "Empirical PCS 3G band", "#8c564b"),
            ("Log-Normal Shadowing", 10.0, 100000.0, "Stochastic Clutter Fading", "#e377c2"),
            ("3GPP TR 38.901 UMi", 500.0, 100000.0, "5G/6G Street Canyon (LoS/NLoS)", "#06b6d4"),
            ("3GPP TR 38.901 UMa", 500.0, 100000.0, "5G/6G Urban Macrocell", "#0284c7"),
            ("3GPP TR 38.901 InH", 500.0, 100000.0, "5G/6G Indoor Mixed Office", "#10b981"),
            ("Close-In (CI) Model", 500.0, 100000.0, "1m Free Space Anchored (mmWave)", "#ca8a04"),
            ("Floating-Intercept (ABG)", 500.0, 100000.0, "3-Parameter Multi-Band Fit", "#4f46e5"),
            ("LoS-NLoS Transition", 500.0, 100000.0, "IEEE Access 2026 Stochastic", "#84cc16"),
        ]

        y_positions = np.arange(len(ranges))

        for idx, (name, fmin, fmax, note, color) in enumerate(ranges):
            ax.barh(idx, fmax - fmin, left=fmin, height=0.55, color=color, alpha=0.85, edgecolor="black", linewidth=0.8)
            ax.text(fmax * 1.08, idx, f"{fmin:.0f} - {fmax:.0f} MHz | {note}", va="center", fontsize=8.5, weight="medium")

        ax.set_yticks(y_positions)
        ax.set_yticklabels([r[0] for r in ranges], weight="bold", fontsize=9.5)
        ax.set_xscale("log")
        ax.set_xlim(0.8, 600000.0)
        ax.set_xlabel("Calibrated Operating Frequency (MHz, Log Scale)")
        ax.set_title("Standardized Propagation Model Calibrated Frequency Ranges (Sub-1 GHz to 100 GHz Sub-THz)")
        ax.grid(True, which="both", ls=":")

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 11. mmWave vs Classical Path Loss at 28 GHz
    def plot_mmwave_vs_classical_distance(
        self, filename: str = "fig11_mmwave_vs_classical_28ghz.png"
    ) -> Path:
        """
        Publication plot: Classical models vs 3GPP UMi LoS/NLoS vs CI vs ABG at 28 GHz.
        """
        fig, ax = plt.subplots(figsize=(9.0, 5.8))
        d_m = np.logspace(1.0, 3.0, 150)  # 10 m to 1000 m
        f_mhz = 28000.0                   # 28 GHz

        fspl_m = FreeSpacePathLoss()
        tworay_m = TwoRayGroundReflection(ht_default=10.0, hr_default=1.5)
        logdist_m = LogDistancePathLoss(n=3.19, d0_m=1.0)
        umi_m = ThreeGPPUMiModel(h_bs=10.0, h_ut=1.5)
        ci_m = CloseInModel(n=3.19, sigma_db=8.2)
        abg_m = FloatingInterceptABGModel()

        pl_fspl = fspl_m.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz")
        pl_tworay = tworay_m.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz")
        pl_logdist = logdist_m.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz")
        pl_umi_los = umi_m.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz", los=True)
        pl_umi_nlos = umi_m.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz", los=False)
        pl_ci = ci_m.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz", los=False)
        pl_abg = abg_m.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz")

        ax.plot(d_m, pl_fspl, label="Free Space (Friis)", color=MODEL_PALETTE["fspl"], lw=2.0, ls="-")
        ax.plot(d_m, pl_tworay, label="Two-Ray Ground Reflection", color=MODEL_PALETTE["two_ray"], lw=2.0, ls="--")
        ax.plot(d_m, pl_logdist, label="Log-Distance (n = 3.19)", color=MODEL_PALETTE["log_distance"], lw=2.0, ls=":")
        ax.plot(d_m, pl_umi_los, label="3GPP TR 38.901 UMi LoS", color=MODEL_PALETTE["three_gpp_umi_los"], lw=2.5, ls="-")
        ax.plot(d_m, pl_umi_nlos, label="3GPP TR 38.901 UMi NLoS", color=MODEL_PALETTE["three_gpp_umi_nlos"], lw=2.5, ls="--")
        ax.plot(d_m, pl_ci, label="Close-In CI (n = 3.19)", color=MODEL_PALETTE["ci"], lw=2.2, ls="-.")
        ax.plot(d_m, pl_abg, label="Floating-Intercept ABG (UMi Preset)", color=MODEL_PALETTE["abg"], lw=2.0, ls=":")

        ax.set_xscale("log")
        ax.set_title("Path Loss vs. Distance at 28 GHz mmWave (Classical vs. 3GPP / CI / ABG)")
        ax.set_xlabel("Horizontal Distance (m, Log Scale)")
        ax.set_ylabel("Path Loss (dB)")
        ax.grid(True, which="both", ls=":")
        ax.legend(loc="upper left", frameon=True, fontsize=9.5)

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 12. Broadband Frequency Sweep 0.5 - 100 GHz
    def plot_broadband_pl_vs_frequency(
        self, fixed_distance_m: float = 200.0, filename: str = "fig12_broadband_pl_vs_frequency.png"
    ) -> Path:
        """
        Publication plot: PL vs frequency from 0.5 to 100 GHz at fixed distance,
        highlighting valid ranges of Hata (<=1.5 GHz) and COST-231 (<=2.0 GHz).
        """
        fig, ax = plt.subplots(figsize=(9.5, 6.0))
        freqs_ghz = np.logspace(np.log10(0.5), np.log10(100.0), 200)
        freqs_mhz = freqs_ghz * 1000.0

        fspl_m = FreeSpacePathLoss()
        umi_m = ThreeGPPUMiModel(h_bs=10.0, h_ut=1.5)
        ci_m = CloseInModel(n=3.19, sigma_db=8.2)
        abg_m = FloatingInterceptABGModel()
        hata_m = HataModel(hb_default=30.0, hm_default=1.5)
        cost_m = COST231HataModel(hb_default=30.0, hm_default=1.5)

        pl_fspl = fspl_m.calculate_path_loss(fixed_distance_m, freqs_mhz, distance_unit="m", frequency_unit="MHz")
        pl_umi_los = umi_m.calculate_path_loss(fixed_distance_m, freqs_mhz, distance_unit="m", frequency_unit="MHz", los=True)
        pl_umi_nlos = umi_m.calculate_path_loss(fixed_distance_m, freqs_mhz, distance_unit="m", frequency_unit="MHz", los=False)
        pl_ci_nlos = ci_m.calculate_path_loss(fixed_distance_m, freqs_mhz, distance_unit="m", frequency_unit="MHz", los=False)
        pl_abg = abg_m.calculate_path_loss(fixed_distance_m, freqs_mhz, distance_unit="m", frequency_unit="MHz")

        # Shaded calibration zones
        ax.axvspan(0.5, 1.5, color="#9467bd", alpha=0.10, label="Okumura-Hata Valid Band (<= 1.5 GHz)")
        ax.axvspan(1.5, 2.0, color="#8c564b", alpha=0.12, label="COST-231 Valid Band (1.5 - 2.0 GHz)")
        ax.axvspan(2.0, 100.0, color="#06b6d4", alpha=0.06, label="5G / 6G Millimeter-Wave & Sub-THz Band")

        # Classical models up to their validity cutoff
        hata_freqs = freqs_mhz[freqs_mhz <= 1500.0]
        pl_hata = hata_m.calculate_path_loss(fixed_distance_m / 1000.0, hata_freqs, distance_unit="km", frequency_unit="MHz", environment="urban_large")
        ax.plot(hata_freqs / 1000.0, pl_hata, color=MODEL_PALETTE["hata"], lw=2.4, ls="-", label="Okumura-Hata (Stops at 1.5 GHz)")
        ax.scatter([1.5], [pl_hata[-1]], color=MODEL_PALETTE["hata"], s=60, zorder=5)

        cost_mask = (freqs_mhz >= 1500.0) & (freqs_mhz <= 2000.0)
        cost_freqs = freqs_mhz[cost_mask]
        pl_cost = cost_m.calculate_path_loss(fixed_distance_m / 1000.0, cost_freqs, distance_unit="km", frequency_unit="MHz", environment="urban_medium")
        ax.plot(cost_freqs / 1000.0, pl_cost, color=MODEL_PALETTE["cost231"], lw=2.4, ls="--", label="COST-231 Hata (Stops at 2.0 GHz)")
        ax.scatter([2.0], [pl_cost[-1]], color=MODEL_PALETTE["cost231"], s=60, zorder=5)

        # 3GPP and modern mmWave models across full 0.5 - 100 GHz
        ax.plot(freqs_ghz, pl_fspl, label="Free Space (Friis)", color=MODEL_PALETTE["fspl"], lw=1.8, ls=":")
        ax.plot(freqs_ghz, pl_umi_los, label="3GPP TR 38.901 UMi LoS", color=MODEL_PALETTE["three_gpp_umi_los"], lw=2.4)
        ax.plot(freqs_ghz, pl_umi_nlos, label="3GPP TR 38.901 UMi NLoS", color=MODEL_PALETTE["three_gpp_umi_nlos"], lw=2.4, ls="--")
        ax.plot(freqs_ghz, pl_ci_nlos, label="Close-In CI NLoS", color=MODEL_PALETTE["ci"], lw=2.0, ls="-.")
        ax.plot(freqs_ghz, pl_abg, label="Floating-Intercept ABG", color=MODEL_PALETTE["abg"], lw=2.0, ls=":")

        ax.set_xscale("log")
        ax.set_title(f"Broadband Frequency Dependence (0.5 GHz to 100 GHz, Distance = {fixed_distance_m:.0f} m)")
        ax.set_xlabel("Carrier Frequency fc (GHz, Log Scale)")
        ax.set_ylabel("Path Loss (dB)")
        ax.grid(True, which="both", ls=":")
        ax.legend(loc="upper left", frameon=True, fontsize=8.8)

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 13. LoS Probability and LoS-NLoS Transition Mixture
    def plot_los_probability_and_mixture(
        self, filename: str = "fig13_los_probability_and_mixture.png"
    ) -> Path:
        """
        Publication plot: P_LoS vs distance and mixed LoS/NLoS channel transitions (IEEE Access 2026).
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 8.0), sharex=True)
        d_m = np.linspace(10.0, 500.0, 200)
        f_mhz = 28000.0  # 28 GHz

        umi = ThreeGPPUMiModel(h_bs=10.0, h_ut=1.5)
        p_los = umi.calculate_los_probability(d_m)

        # Top: LoS Probability
        ax1.plot(d_m, p_los, color="#0284c7", lw=2.5, label="3GPP UMi LoS Probability P_LoS(d)")
        ax1.axvline(18.0, color="#e11d48", ls="--", alpha=0.8, label="LoS Horizon: d2D = 18 m (P_LoS = 1.0)")
        ax1.set_ylabel("LoS Probability P_LoS")
        ax1.set_title("LoS Probability Roll-Off & Channel State Mixture (28 GHz mmWave, IEEE Access 2026)")
        ax1.grid(True, ls=":")
        ax1.set_ylim(-0.05, 1.05)
        ax1.legend(loc="upper right", frameon=True)

        # Bottom: Path Loss & Mixed Channel Transitions
        pl_los = umi.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz", los=True)
        pl_nlos = umi.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz", los=False)

        trans_model = StatisticalLoSNLoSTransitionModel(hbs_default=10.0, hut_default=1.5, seed=42)
        pl_mean = trans_model.calculate_path_loss(d_m, f_mhz, distance_unit="m", frequency_unit="MHz", mode="expectation")

        # Realization traces (corner turnings)
        realizations = trans_model.generate_transition_realizations(d_m, f_mhz, num_realizations=4, distance_unit="m", frequency_unit="MHz", seed=42)
        for i, real in enumerate(realizations):
            ax2.plot(d_m, real, color="gray", alpha=0.35, lw=1.2, ls="--", label="Monte Carlo Realization" if i == 0 else "")

        ax2.plot(d_m, pl_los, color=MODEL_PALETTE["three_gpp_umi_los"], lw=2.0, ls="-", label="Pure LoS State")
        ax2.plot(d_m, pl_nlos, color=MODEL_PALETTE["three_gpp_umi_nlos"], lw=2.0, ls="--", label="Pure NLoS State")
        ax2.plot(d_m, pl_mean, color="#84cc16", lw=2.8, ls="-", label="Probabilistic Expected Mean (IEEE Access 2026)")

        ax2.set_xlabel("Horizontal Distance d2D (m)")
        ax2.set_ylabel("Path Loss (dB)")
        ax2.grid(True, ls=":")
        ax2.legend(loc="lower right", frameon=True, fontsize=9.0)

        save_path = self.output_dir / filename
        fig.tight_layout()
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 14. Benchmark Bar Chart at 3.5 GHz and 28 GHz
    def plot_benchmark_barchart_5g_mmwave(
        self, filename: str = "fig14_benchmark_barchart_3_5ghz_and_28ghz.png"
    ) -> Path:
        """
        Grouped bar chart benchmarking propagation models at 3.5 GHz and 28 GHz.
        """
        fig, ax = plt.subplots(figsize=(10.0, 5.8))

        models = ["Free Space", "3GPP UMi LoS", "3GPP UMi NLoS", "Close-In (CI)", "ABG Model", "LoS-NLoS Trans."]
        
        # 3.5 GHz (d = 200 m)
        d_35 = 200.0
        f_35 = 3500.0
        fspl_35 = FreeSpacePathLoss().calculate_path_loss(d_35, f_35, "m", "MHz")
        umi_35 = ThreeGPPUMiModel(h_bs=10.0, h_ut=1.5)
        umi_los_35 = umi_35.calculate_path_loss(d_35, f_35, "m", "MHz", los=True)
        umi_nlos_35 = umi_35.calculate_path_loss(d_35, f_35, "m", "MHz", los=False)
        ci_35 = CloseInModel().calculate_path_loss(d_35, f_35, "m", "MHz", los=False)
        abg_35 = FloatingInterceptABGModel().calculate_path_loss(d_35, f_35, "m", "MHz")
        trans_35 = StatisticalLoSNLoSTransitionModel(hbs_default=10.0, hut_default=1.5).calculate_path_loss(d_35, f_35, "m", "MHz", mode="expectation")

        vals_35 = [float(fspl_35), float(umi_los_35), float(umi_nlos_35), float(ci_35), float(abg_35), float(trans_35)]

        # 28 GHz (d = 100 m)
        d_28 = 100.0
        f_28 = 28000.0
        fspl_28 = FreeSpacePathLoss().calculate_path_loss(d_28, f_28, "m", "MHz")
        umi_28 = ThreeGPPUMiModel(h_bs=10.0, h_ut=1.5)
        umi_los_28 = umi_28.calculate_path_loss(d_28, f_28, "m", "MHz", los=True)
        umi_nlos_28 = umi_28.calculate_path_loss(d_28, f_28, "m", "MHz", los=False)
        ci_28 = CloseInModel().calculate_path_loss(d_28, f_28, "m", "MHz", los=False)
        abg_28 = FloatingInterceptABGModel().calculate_path_loss(d_28, f_28, "m", "MHz")
        trans_28 = StatisticalLoSNLoSTransitionModel(hbs_default=10.0, hut_default=1.5).calculate_path_loss(d_28, f_28, "m", "MHz", mode="expectation")

        vals_28 = [float(fspl_28), float(umi_los_28), float(umi_nlos_28), float(ci_28), float(abg_28), float(trans_28)]

        x = np.arange(len(models))
        width = 0.36

        rects1 = ax.bar(x - width/2, vals_35, width, label="5G Mid-Band: 3.5 GHz (d = 200 m)", color="#0284c7", edgecolor="black")
        rects2 = ax.bar(x + width/2, vals_28, width, label="5G/6G mmWave: 28 GHz (d = 100 m)", color="#e11d48", edgecolor="black")

        for rect in rects1:
            h = rect.get_height()
            ax.annotate(f"{h:.1f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, weight="bold")

        for rect in rects2:
            h = rect.get_height()
            ax.annotate(f"{h:.1f}", xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, weight="bold")

        ax.set_ylabel("Path Loss (dB)")
        ax.set_title("5G Mid-Band (3.5 GHz) vs mmWave (28 GHz) Model Benchmark Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels(models, rotation=15, ha="right", weight="medium")
        ax.set_ylim(0, max(vals_35 + vals_28) * 1.18)
        ax.legend(loc="upper left", frameon=True)
        ax.grid(axis="y", ls=":")

        save_path = self.output_dir / filename
        fig.tight_layout()
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

    # 10. Summary Comparison Bar Chart
    def plot_summary_comparison_chart(
        self, sim_result: SimulationResult, target_distance: float = 3.0, filename: str = "fig10_summary_comparison_chart.png"
    ) -> Path:
        fig, ax = plt.subplots(figsize=(9, 5.5))

        # Find closest index to target distance
        idx = np.argmin(np.abs(sim_result.sweep_values - target_distance))
        actual_d = sim_result.sweep_values[idx]

        models = []
        path_losses = []
        colors = []

        for key, pl_arr in sim_result.path_loss_db.items():
            models.append(MODEL_LABELS.get(key, key))
            path_losses.append(pl_arr[idx])
            colors.append(MODEL_PALETTE.get(key, "#333333"))

        bars = ax.bar(models, path_losses, color=colors, edgecolor="black", width=0.55)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.1f} dB",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=10, weight="bold")

        ax.set_title(f"Predicted Path Loss Comparison at d = {actual_d:.1f} {sim_result.sweep_unit} ({sim_result.scenario_name})")
        ax.set_ylabel("Path Loss (dB)")
        ax.set_ylim(0, max(path_losses) * 1.15)
        ax.set_xticks(range(len(models)))
        ax.set_xticklabels(models, rotation=25, ha="right")
        ax.grid(axis="y", ls=":")

        save_path = self.output_dir / filename
        fig.savefig(save_path)
        plt.close(fig)
        return save_path

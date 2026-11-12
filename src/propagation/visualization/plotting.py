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
from propagation.models.hata import HataModel
from propagation.models.shadowing import LogNormalShadowing
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
        fig, ax = plt.subplots(figsize=(10, 6.0))

        # Model frequency intervals (MHz)
        ranges = [
            ("Free Space (Friis)", 1.0, 60000.0, "Theoretical LOS"),
            ("Two-Ray Ground Refl.", 1.0, 60000.0, "Multipath Flat Earth"),
            ("Log-Distance", 10.0, 60000.0, "Parametric"),
            ("Okumura Model", 150.0, 1920.0, "Empirical (Tokyo)"),
            ("Okumura-Hata", 150.0, 1500.0, "Empirical Macrocell"),
            ("COST-231 Hata", 1500.0, 2000.0, "Empirical PCS"),
            ("Log-Normal Shadowing", 10.0, 60000.0, "Stochastic Fading"),
        ]

        y_positions = np.arange(len(ranges))
        bar_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]

        for idx, (name, fmin, fmax, note) in enumerate(ranges):
            ax.barh(idx, fmax - fmin, left=fmin, height=0.5, color=bar_colors[idx], alpha=0.85, edgecolor="black")
            ax.text(fmax * 1.05, idx, f"{fmin:.0f} - {fmax:.0f} MHz ({note})", va="center", fontsize=9, weight="medium")

        ax.set_yticks(y_positions)
        ax.set_yticklabels([r[0] for r in ranges], weight="bold")
        ax.set_xscale("log")
        ax.set_xlim(0.8, 200000.0)
        ax.set_xlabel("Calibrated Operating Frequency (MHz, Log Scale)")
        ax.set_title("Propagation Model Calibrated Frequency Applicability Ranges")
        ax.grid(True, which="both", ls=":")

        save_path = self.output_dir / filename
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

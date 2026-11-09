"""
Batch Figure Generation Script.

Executes numerical simulations and generates all 10 publication-quality
scientific figures, saving them into outputs/figures/.
"""

import sys
from pathlib import Path

# Ensure src is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from propagation.simulation.scenario import ScenarioConfig
from propagation.simulation.engine import SimulationEngine
from propagation.visualization.plotting import Visualizer


def main():
    print("=" * 70)
    print("  WIRELESS SIGNAL PROPAGATION MODELS: BATCH FIGURE GENERATOR")
    print("=" * 70)

    output_dir = ROOT_DIR / "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    visualizer = Visualizer(output_dir=output_dir)

    print("\n[1/4] Loading Simulation Scenarios...")
    urban_cfg = ScenarioConfig.from_yaml(ROOT_DIR / "experiments" / "scenarios" / "urban.yaml")
    engine = SimulationEngine()

    print("[2/4] Running Numerical Sweeps...")
    urban_sim = engine.run_distance_sweep(urban_cfg)
    freq_sim = engine.run_frequency_sweep(
        urban_cfg, min_freq_mhz=150.0, max_freq_mhz=3500.0, num_freq_points=150, fixed_distance_km=2.0
    )

    print("[3/4] Rendering Scientific Figures...")
    generated_plots = []

    # Plot 1: Path loss vs distance
    p1 = visualizer.plot_path_loss_vs_distance(urban_sim)
    generated_plots.append(("Fig 1", "Path Loss vs Distance", p1.name))

    # Plot 2: Received power vs distance
    p2 = visualizer.plot_received_power_vs_distance(urban_sim)
    generated_plots.append(("Fig 2", "Received Power vs Distance", p2.name))

    # Plot 3: Path loss vs frequency
    p3 = visualizer.plot_path_loss_vs_frequency(freq_sim)
    generated_plots.append(("Fig 3", "Path Loss vs Frequency", p3.name))

    # Plot 4: Environmental comparison
    p4 = visualizer.plot_environmental_comparison()
    generated_plots.append(("Fig 4", "Environmental Comparison", p4.name))

    # Plot 5: Model difference plot
    p5 = visualizer.plot_model_difference(urban_sim, baseline_key="fspl")
    generated_plots.append(("Fig 5", "Model Difference vs Free Space", p5.name))

    # Plot 6: Shadowing distribution and realizations
    p6 = visualizer.plot_shadowing_analysis()
    generated_plots.append(("Fig 6", "Log-Normal Shadowing Distribution", p6.name))

    # Plot 7: Antenna height sensitivity
    p7 = visualizer.plot_antenna_height_sensitivity()
    generated_plots.append(("Fig 7", "Antenna Height Sensitivity", p7.name))

    # Plot 8: 2D Heatmap
    p8 = visualizer.plot_path_loss_2d_heatmap()
    generated_plots.append(("Fig 8", "Path Loss 2D Heatmap", p8.name))

    # Plot 9: Model applicability matrix
    p9 = visualizer.plot_model_applicability_matrix()
    generated_plots.append(("Fig 9", "Model Applicability Ranges", p9.name))

    # Plot 10: Summary comparison chart
    p10 = visualizer.plot_summary_comparison_chart(urban_sim, target_distance=3.0)
    generated_plots.append(("Fig 10", "Summary Comparison Bar Chart", p10.name))

    print("\n[4/4] Generation Complete! Summary:")
    print("-" * 70)
    print(f"{'Figure ID':<10} | {'Description':<35} | {'Filename':<30}")
    print("-" * 70)
    for fig_id, desc, filename in generated_plots:
        print(f"{fig_id:<10} | {desc:<35} | {filename:<30}")
    print("-" * 70)
    print(f"All 10 figures successfully stored in: {output_dir}\n")


if __name__ == "__main__":
    main()


"""
Script to create the 4 required research Jupyter notebooks with full markdown narrative and code.
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.12.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }


def md_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }


def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    }


def build_01_model_exploration():
    cells = [
        md_cell(
            "# 01. Wireless Signal Propagation: Model Exploration\n\n"
            "This notebook introduces and validates each of the **seven propagation models** "
            "implemented in the `propagation` framework:\n\n"
            "1. Free Space Path Loss (Friis)\n"
            "2. Two-Ray Ground Reflection\n"
            "3. Log-Distance Path Loss\n"
            "4. Okumura Model\n"
            "5. Okumura-Hata Model\n"
            "6. COST-231 Hata Model\n"
            "7. Log-Normal Shadowing"
        ),
        code_cell(
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "# Ensure src is discoverable\n"
            "ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
            "sys.path.insert(0, str(ROOT / 'src'))\n\n"
            "from propagation.models import (\n"
            "    FreeSpacePathLoss, TwoRayGroundReflection, LogDistancePathLoss,\n"
            "    OkumuraModel, HataModel, COST231HataModel, LogNormalShadowing\n"
            ")\n"
            "from propagation.core.units import wavelength\n\n"
            "print('Models successfully loaded!')"
        ),
        md_cell(
            "### 1. Free Space Path Loss (Friis Model)\n\n"
            "The Friis equation predicts line-of-sight path loss in an ideal lossless vacuum:\n\n"
            "$$PL_{FS}(d) = 20\\log_{10}(d) + 20\\log_{10}(f) + 20\\log_{10}\\left(\\frac{4\\pi}{c}\\right)$$"
        ),
        code_cell(
            "fspl = FreeSpacePathLoss()\n"
            "d_km = np.linspace(0.1, 10.0, 100)\n"
            "f_mhz = 900.0\n\n"
            "pl_fspl = fspl.calculate_path_loss(d_km, f_mhz, distance_unit='km', frequency_unit='MHz')\n\n"
            "plt.figure(figsize=(7, 4))\n"
            "plt.plot(d_km, pl_fspl, 'b-', lw=2, label='Friis FSPL (900 MHz)')\n"
            "plt.xlabel('Distance (km)')\n"
            "plt.ylabel('Path Loss (dB)')\n"
            "plt.title('Free Space Path Loss vs Distance')\n"
            "plt.grid(True, ls=':')\n"
            "plt.legend()\n"
            "plt.show()"
        ),
        md_cell(
            "### 2. Two-Ray Ground Reflection Model\n\n"
            "Combines direct LOS ray and single earth specular reflected ray. Asymptotically decays as $d^{-4}$ beyond crossover distance $d_c$."
        ),
        code_cell(
            "two_ray = TwoRayGroundReflection(ht_default=40.0, hr_default=2.0)\n"
            "d_c = two_ray.crossover_distance(ht=40.0, hr=2.0, frequency_hz=900e6)\n"
            "print(f'Crossover distance d_c = {d_c:.1f} meters ({d_c/1000:.2f} km)')\n\n"
            "pl_exact = two_ray.calculate_path_loss(d_km, f_mhz, distance_unit='km', frequency_unit='MHz', mode='exact')\n"
            "pl_asymp = two_ray.calculate_path_loss(d_km, f_mhz, distance_unit='km', frequency_unit='MHz', mode='asymptotic')\n\n"
            "plt.figure(figsize=(7, 4))\n"
            "plt.plot(d_km, pl_exact, 'orange', lw=1.8, label='Two-Ray Exact Multipath')\n"
            "plt.plot(d_km, pl_asymp, 'k--', lw=1.8, label='Two-Ray Asymptotic (d^-4)')\n"
            "plt.axvline(d_c/1000, color='red', ls=':', label=f'Crossover dc = {d_c/1000:.2f} km')\n"
            "plt.xlabel('Distance (km)')\n"
            "plt.ylabel('Path Loss (dB)')\n"
            "plt.title('Two-Ray Ground Reflection Behavior')\n"
            "plt.grid(True, ls=':')\n"
            "plt.legend()\n"
            "plt.show()"
        ),
        md_cell(
            "### 3. Log-Distance Path Loss Model\n\n"
            "$$PL(d) = PL(d_0) + 10 n \\log_{10}(d / d_0)$$"
        ),
        code_cell(
            "log_dist_urban = LogDistancePathLoss(environment='urban')\n"
            "log_dist_indoor = LogDistancePathLoss(environment='indoor_obstructed')\n\n"
            "pl_urb = log_dist_urban.calculate_path_loss(d_km, f_mhz, distance_unit='km', frequency_unit='MHz')\n"
            "print(f'Urban exponent n = {log_dist_urban.n}, Indoor obstructed n = {log_dist_indoor.n}')"
        ),
        md_cell(
            "### 4-6. Empirical Models: Okumura, Hata, and COST-231\n\n"
            "Comparing classical empirical macrocell formulations in an urban environment at 1800 MHz."
        ),
        code_cell(
            "okumura = OkumuraModel(hte_default=30.0, hre_default=1.5, environment='urban')\n"
            "hata = HataModel(hb_default=30.0, hm_default=1.5, environment='urban_medium')\n"
            "cost231 = COST231HataModel(hb_default=30.0, hm_default=1.5, environment='medium_city')\n\n"
            "pl_oku = okumura.calculate_path_loss(d_km, 1800.0, distance_unit='km', frequency_unit='MHz')\n"
            "pl_hata = hata.calculate_path_loss(d_km, 1800.0, distance_unit='km', frequency_unit='MHz')\n"
            "pl_cost = cost231.calculate_path_loss(d_km, 1800.0, distance_unit='km', frequency_unit='MHz')\n\n"
            "plt.figure(figsize=(7, 4))\n"
            "plt.plot(d_km, pl_oku, 'r:', lw=2, label='Okumura (1800 MHz)')\n"
            "plt.plot(d_km, pl_hata, 'm-', lw=2, label='Okumura-Hata (1800 MHz Extrap.)')\n"
            "plt.plot(d_km, pl_cost, 'brown', lw=2, ls='--', label='COST-231 Hata (1800 MHz)')\n"
            "plt.xlabel('Distance (km)')\n"
            "plt.ylabel('Path Loss (dB)')\n"
            "plt.title('Empirical Cellular Model Comparison (1800 MHz)')\n"
            "plt.grid(True, ls=':')\n"
            "plt.legend()\n"
            "plt.show()"
        ),
        md_cell(
            "### 7. Stochastic Log-Normal Shadowing\n\n"
            "$$PL(d) = \\overline{PL}(d) + X_\\sigma, \\quad X_\\sigma \\sim \\mathcal{N}(0, \\sigma^2)$$"
        ),
        code_cell(
            "shadow = LogNormalShadowing(n=3.0, sigma_db=6.0, seed=42)\n"
            "realizations = shadow.generate_realizations(d_km, 1800.0, num_realizations=5, distance_unit='km', frequency_unit='MHz')\n"
            "mean_pl, lower_95, upper_95 = shadow.calculate_bounds(d_km, 1800.0, confidence=0.95, distance_unit='km', frequency_unit='MHz')\n\n"
            "plt.figure(figsize=(7, 4))\n"
            "for i in range(len(realizations)):\n"
            "    plt.plot(d_km, realizations[i], color='gray', alpha=0.4, lw=1.0)\n"
            "plt.plot(d_km, mean_pl, 'b-', lw=2.2, label='Deterministic Mean')\n"
            "plt.fill_between(d_km, lower_95, upper_95, color='b', alpha=0.15, label='95% Confidence Bounds (+/- 1.96 sigma)')\n"
            "plt.xlabel('Distance (km)')\n"
            "plt.ylabel('Path Loss (dB)')\n"
            "plt.title('Log-Normal Shadowing Realizations (sigma = 6 dB)')\n"
            "plt.grid(True, ls=':')\n"
            "plt.legend()\n"
            "plt.show()"
        )
    ]
    with open(NOTEBOOKS_DIR / "01_model_exploration.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(cells), f, indent=1)


def build_02_model_comparison():
    cells = [
        md_cell(
            "# 02. Multi-Model Comparative Analysis\n\n"
            "Executes scenario-based comparisons across models under identical transmitter/receiver "
            "power parameters, distances, and carrier frequencies."
        ),
        code_cell(
            "import sys\n"
            "from pathlib import Path\n"
            "import matplotlib.pyplot as plt\n\n"
            "ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
            "sys.path.insert(0, str(ROOT / 'src'))\n\n"
            "from propagation.simulation.scenario import ScenarioConfig\n"
            "from propagation.simulation.engine import SimulationEngine\n"
            "from propagation.analysis.comparator import ModelComparator\n\n"
            "# Load Urban Scenario\n"
            "urban_cfg = ScenarioConfig.from_yaml(ROOT / 'experiments' / 'scenarios' / 'urban.yaml')\n"
            "engine = SimulationEngine()\n"
            "urban_sim = engine.run_distance_sweep(urban_cfg)\n\n"
            "print(f'Simulation completed for scenario: {urban_sim.scenario_name}')"
        ),
        md_cell("### Descriptive Statistics Summary Table"),
        code_cell(
            "stats_df = ModelComparator.calculate_summary_statistics(urban_sim)\n"
            "display(stats_df) if 'display' in globals() else print(stats_df)"
        ),
        md_cell("### Discrepancy Relative to Free Space (Delta PL = PL_model - PL_FSPL)"),
        code_cell(
            "diff_df = ModelComparator.calculate_pairwise_differences(urban_sim, baseline_model='fspl')\n"
            "display(diff_df.head()) if 'display' in globals() else print(diff_df.head())"
        ),
        code_cell(
            "plt.figure(figsize=(8, 5))\n"
            "d_vals = urban_sim.sweep_values\n"
            "for col in diff_df.columns:\n"
            "    if col.startswith('Delta_PL'):\n"
            "        plt.plot(d_vals, diff_df[col], lw=2.0, label=col.replace('Delta_PL_', '').replace('_dB', ''))\n"
            "plt.xlabel('Distance (km)')\n"
            "plt.ylabel('Excess Path Loss over Free Space (dB)')\n"
            "plt.title('Urban Clutter Excess Path Loss Discrepancy')\n"
            "plt.xscale('log')\n"
            "plt.grid(True, which='both', ls=':')\n"
            "plt.legend()\n"
            "plt.show()"
        )
    ]
    with open(NOTEBOOKS_DIR / "02_model_comparison.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(cells), f, indent=1)


def build_03_sensitivity_analysis():
    cells = [
        md_cell(
            "# 03. Parameter Sensitivity Analysis\n\n"
            "Investigates the sensitivity of predicted path loss to:\n"
            "- Base station antenna height ($h_t$)\n"
            "- Mobile antenna height ($h_r$)\n"
            "- Carrier frequency ($f$)\n"
            "- Path loss exponent ($n$)"
        ),
        code_cell(
            "import sys\n"
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n\n"
            "ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
            "sys.path.insert(0, str(ROOT / 'src'))\n\n"
            "from propagation.analysis.sensitivity import SensitivityAnalyzer\n\n"
            "# 1. Base Station Height Sensitivity Sweep\n"
            "df_ht = SensitivityAnalyzer.sweep_tx_antenna_height(\n"
            "    min_ht_m=20.0, max_ht_m=200.0, num_points=50, distance_km=5.0, frequency_mhz=900.0\n"
            ")\n\n"
            "plt.figure(figsize=(7, 4.5))\n"
            "plt.plot(df_ht['tx_height_m'], df_ht['PL_TwoRay_dB'], 'orange', lw=2, label='Two-Ray Ground Refl.')\n"
            "plt.plot(df_ht['tx_height_m'], df_ht['PL_Okumura_dB'], 'red', lw=2, ls=':', label='Okumura')\n"
            "plt.plot(df_ht['tx_height_m'], df_ht['PL_Hata_dB'], 'purple', lw=2, ls='--', label='Okumura-Hata')\n"
            "plt.xlabel('Base Station Antenna Height ht (m)')\n"
            "plt.ylabel('Path Loss (dB)')\n"
            "plt.title('Path Loss Sensitivity to Base Station Antenna Height (d = 5 km)')\n"
            "plt.grid(True, ls=':')\n"
            "plt.legend()\n"
            "plt.show()"
        ),
        md_cell("### 2D Parameter Heatmap: Distance vs Carrier Frequency"),
        code_cell(
            "D, F, PL = SensitivityAnalyzer.generate_2d_heatmap_grid(\n"
            "    model_name='cost231',\n"
            "    distances_km=np.linspace(1.0, 15.0, 50),\n"
            "    frequencies_mhz=np.linspace(1500.0, 2000.0, 50)\n"
            ")\n\n"
            "plt.figure(figsize=(8, 5.5))\n"
            "contour = plt.contourf(D, F, PL, levels=25, cmap='plasma')\n"
            "cbar = plt.colorbar(contour)\n"
            "cbar.set_label('Path Loss (dB)')\n"
            "plt.xlabel('Distance (km)')\n"
            "plt.ylabel('Frequency (MHz)')\n"
            "plt.title('COST-231 Hata 2D Path Loss Parameter Space')\n"
            "plt.show()"
        )
    ]
    with open(NOTEBOOKS_DIR / "03_sensitivity_analysis.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(cells), f, indent=1)


def build_04_final_results():
    cells = [
        md_cell(
            "# 04. Final Results and Research Synthesis\n\n"
            "Synthesizes publication-ready comparative metrics, formal comparison taxonomy, "
            "and scientific recommendations for wireless systems engineering."
        ),
        code_cell(
            "import sys\n"
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n\n"
            "ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path.cwd()\n"
            "sys.path.insert(0, str(ROOT / 'src'))\n\n"
            "from propagation.analysis.comparator import ModelComparator\n"
            "from propagation.visualization.plotting import Visualizer\n"
            "from propagation.simulation.scenario import ScenarioConfig\n"
            "from propagation.simulation.engine import SimulationEngine\n\n"
            "comp_table = ModelComparator.get_comparison_table()\n"
            "display(comp_table) if 'display' in globals() else print(comp_table)"
        ),
        md_cell("### Summary Path Loss at Benchmark Cell Edge (d = 3 km, Urban Macrocell)"),
        code_cell(
            "urban_cfg = ScenarioConfig.from_yaml(ROOT / 'experiments' / 'scenarios' / 'urban.yaml')\n"
            "engine = SimulationEngine()\n"
            "urban_sim = engine.run_distance_sweep(urban_cfg)\n\n"
            "vis = Visualizer(output_dir=ROOT / 'outputs' / 'figures')\n"
            "chart_path = vis.plot_summary_comparison_chart(urban_sim, target_distance=3.0)\n"
            "print(f'Figure saved: {chart_path}')"
        )
    ]
    with open(NOTEBOOKS_DIR / "04_final_results.ipynb", "w", encoding="utf-8") as f:
        json.dump(make_notebook(cells), f, indent=1)


def main():
    print("Generating 4 research Jupyter notebooks...")
    build_01_model_exploration()
    build_02_model_comparison()
    build_03_sensitivity_analysis()
    build_04_final_results()
    print("All 4 notebooks generated successfully!")


if __name__ == "__main__":
    main()


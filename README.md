# Comparative Analysis of Wireless Signal Propagation Models

[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/tests-32%20passed-brightgreen.svg)]()
[![Code Style](https://img.shields.io/badge/code%20style-pep8-green.svg)]()

A comprehensive, scientific, and reproducible Python simulation framework for evaluating, comparing, and analyzing wireless signal propagation models across diverse carrier frequencies, distances, antenna configurations, and propagation environments.

---

## Overview

In wireless communications, accurate prediction of path loss and received signal power is fundamental to network dimensioning, cell-site placement, link budget verification, and coverage reliability analysis. 

This repository provides an end-to-end research-oriented platform that implements seven classical and modern wireless propagation models:
- **Theoretical Models:** Friis Free Space Path Loss (FSPL), Two-Ray Ground Reflection
- **Empirical Models:** Log-Distance Path Loss, Okumura Model, Okumura-Hata Model, COST-231 Hata Model
- **Stochastic Models:** Log-Normal Shadow Fading (with Monte Carlo simulation and analytical outage probability)

---

## Problem Statement

Wireless system engineers and researchers frequently face the challenge of selecting an appropriate propagation model for a specific operational frequency, distance, antenna height, and terrain. 

Theoretical models (such as Free Space) often severely underestimate propagation loss in cluttered terrestrial environments, while classical empirical models (such as Okumura-Hata) have strict frequency and distance calibration bounds that cannot be naively extrapolated to modern sub-6 GHz or 5G systems. 

Without a unified comparative framework, engineers risk deploying networks with severe coverage blackspots or unmanageable co-channel interference.

---

## Objectives

1. Implement seven independent, reusable, and rigorously validated wireless propagation models adhering to a common abstract interface.
2. Develop a vectorized numerical simulation engine capable of distance sweeps, frequency sweeps, and link budget evaluations.
3. Quantitatively analyze model divergence, excess path loss relative to free space, and the two-ray crossover distance $d_c$.
4. Evaluate environmental clutter penalties across urban, suburban, rural, and indoor scenarios.
5. Model spatial shadow fading through Monte Carlo realizations and derive closed-form link outage probabilities.
6. Provide an automated testing suite, interactive Jupyter notebooks, publication-grade visualization tools, an academic PowerPoint generator, and an interactive Streamlit dashboard.

---

## Models Implemented

| Model | Classification | Complexity | Environment | Calibrated Freq | Calibrated Dist |
|---|---|---|---|---|---|
| **Free Space (Friis)** | Theoretical | $\mathcal{O}(1)$ Closed-form | Unobstructed LOS | Broadband | Far-field ($d > 0$) |
| **Two-Ray Ground Reflection** | Theoretical | $\mathcal{O}(1)$ Vector / Asymp | Flat earth, waterways | 1 MHz – 60 GHz | 1 m – 100 km |
| **Log-Distance Path Loss** | Empirical | $\mathcal{O}(1)$ Parametric | In-building, microcell | Calibrated | $d \ge d_0$ |
| **Okumura Model** | Empirical | $\mathcal{O}(1)$ Empirical Fit | Urban/Suburban macrocell | 150 – 1920 MHz | 1 – 100 km |
| **Okumura-Hata Model** | Empirical | $\mathcal{O}(1)$ Analytical | Urban, suburban, rural | 150 – 1500 MHz | 1 – 20 km |
| **COST-231 Hata Model** | Empirical | $\mathcal{O}(1)$ Analytical | Medium & metropolitan city | 1500 – 2000 MHz | 1 – 20 km |
| **Log-Normal Shadowing** | Stochastic | $\mathcal{O}(N)$ Monte Carlo | Cluttered terrain | All bands | $d \ge d_0$ |

---

## System Architecture

```text
src/
└── propagation/
    ├── core/                  # Unit conversions, RF constants, link budget equations
    ├── models/                # Abstract base class & 7 concrete propagation models
    ├── simulation/            # ScenarioConfig YAML loader & SimulationEngine sweeps
    ├── analysis/              # Pairwise difference comparator, sensitivity sweeps, statistics
    └── visualization/         # Publication-grade Matplotlib / Seaborn plotting engine
```

---

## Mathematical Background

### Free Space Path Loss (Friis)
$$PL_{\text{FS}}(d, f) = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}\left(\frac{4\pi}{c}\right)$$

### Two-Ray Ground Reflection (Asymptotic)
Beyond crossover distance $d_c = \frac{4\pi h_t h_r}{\lambda}$:
$$PL_{\text{Two-Ray}}(d) = 40\log_{10}(d) - 20\log_{10}(h_t) - 20\log_{10}(h_r)$$

### Log-Distance Path Loss
$$PL(d) = PL(d_0) + 10 n \log_{10}\left(\frac{d}{d_0}\right)$$

### Okumura-Hata Urban Model
$$PL_{\text{urban}} = 69.55 + 26.16\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d)$$

### COST-231 Hata Model
$$PL_{\text{COST}} = 46.3 + 33.9\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d) + C_M$$

### Log-Normal Shadowing & Outage Probability
$$PL(d) = \overline{PL}(d) + X_\sigma, \quad X_\sigma \sim \mathcal{N}(0, \sigma^2)$$
$$P_{\text{outage}} = Q\left(\frac{\overline{P}_r - \gamma_{\text{th}}}{\sigma}\right) = \frac{1}{2} \text{erfc}\left(\frac{\overline{P}_r - \gamma_{\text{th}}}{\sqrt{2}\sigma}\right)$$

---

## Features

- **Strict Unit Safety:** Seamless, vectorized conversions between Hz, MHz, GHz, meters, kilometers, Watts, milliwatts, and dBm.
- **Dynamic Boundary Warnings:** Emits non-terminating warnings (`ModelRangeWarning`) when inputs exceed empirical calibration limits, preventing invalid extrapolations.
- **Reproducible Simulations:** Seed-controlled pseudo-random number generation for Monte Carlo shadow fading and realization trajectories.
- **Tidy Data Export:** Exports full numerical simulation results to CSV and Pandas DataFrames.
- **10 Publication-Quality Plots:** Automated high-resolution figure generator (300 DPI) for reports and research papers.
- **Hard-Copy PDF Report Generator:** Compiles simulation results and figures into an academic research report.
- **Academic Slide Deck:** Automatically compiles a 15-slide PowerPoint deck (`.pptx`) embedding actual simulation charts.
- **Interactive Web App:** Streamlit dashboard for real-time parameter tuning.

---

## Project Structure

```text
├── experiments/scenarios/     # Predefined scenario YAML configurations
├── scripts/                   # CLI scripts for simulation, plotting, report & PPT
├── notebooks/                 # 4 Jupyter research notebooks
├── src/propagation/           # Core library source code
├── tests/                     # 32 pytest unit and integration tests
├── outputs/figures/           # 10 generated PNG figures (300 DPI)
├── outputs/reports/           # Generated CSV data and PDF hard-copy report
├── outputs/presentation/      # Generated PowerPoint presentation (.pptx)
└── docs/                      # Comprehensive theoretical and architectural documentation
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/wireless-propagation-analysis.git
cd wireless-propagation-analysis

# Create virtual environment (optional)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies and package in editable mode
pip install -r requirements.txt
pip install -e .
```

---

## Usage

### 1. Running Simulations via CLI
```bash
# Run specific scenario
python scripts/run_simulation.py --scenario urban
python scripts/run_simulation.py --scenario rural
python scripts/run_simulation.py --scenario indoor
python scripts/run_simulation.py --scenario suburban
python scripts/run_simulation.py --scenario 5g_midband

# Run all scenarios
python scripts/run_simulation.py --scenario all
```

### 2. Generating Scientific Figures
```bash
python scripts/generate_figures.py
```
*Generates all 10 figures in `outputs/figures/`.*

### 3. Generating Hard-Copy PDF Report
```bash
python scripts/generate_report.py
```
*Outputs `outputs/reports/Wireless_Propagation_Comparative_Report.pdf`.*

### 4. Generating Academic Presentation (PPT)
```bash
python scripts/generate_presentation.py
```
*Outputs `outputs/presentation/Wireless_Propagation_Analysis.pptx`.*

### 5. Launching Streamlit Interactive Dashboard
```bash
streamlit run app.py
```

---

## Example Results

### Urban Macrocell Benchmark ($f = 1800\text{ MHz}$, $h_t = 30\text{ m}$, $h_r = 1.5\text{ m}$, $P_t = 43\text{ dBm}$)

| Model | Path Loss at 1 km (dB) | Path Loss at 5 km (dB) | Path Loss at 10 km (dB) | Received Power at 10 km (dBm) |
|---|---|---|---|---|
| **Free Space** | 97.6 | 111.5 | 117.6 | -62.6 |
| **Two-Ray** | 95.2 | 113.8 | 127.0 | -72.0 |
| **Log-Distance ($n=3.2$)** | 133.6 | 155.9 | 165.6 | -110.6 |
| **Okumura** | 142.4 | 163.5 | 172.2 | -117.2 |
| **Okumura-Hata** | 134.3 | 160.7 | 169.5 | -114.5 |
| **COST-231 Hata** | 136.2 | 162.6 | 171.4 | -116.4 |

*At a 10 km cell edge, COST-231 Hata predicts **53.8 dB higher path loss** than Free Space due to severe urban building diffraction and clutter absorption.*

---

## Visualization

The framework generates 10 figures stored under `outputs/figures/`:
1. `fig01_path_loss_vs_distance.png`: Comparative path loss across all models on log distance scale.
2. `fig02_received_power_vs_distance.png`: Received signal power with receiver sensitivity threshold.
3. `fig03_path_loss_vs_frequency.png`: Carrier frequency sensitivity from 150 MHz to 3.5 GHz.
4. `fig04_environmental_comparison.png`: Urban Large, Urban Medium, Suburban, and Rural terrain curves.
5. `fig05_model_difference_vs_baseline.png`: Excess path loss discrepancy relative to Free Space.
6. `fig06_shadowing_distribution.png`: Log-normal Monte Carlo trajectories and Gaussian probability density function.
7. `fig07_antenna_height_sensitivity.png`: Impact of transmitter height $h_t$ (20–200 m) and receiver height $h_r$ (1–10 m).
8. `fig08_path_loss_2d_heatmap.png`: 2D parameter space heatmap of path loss over distance and frequency.
9. `fig09_model_applicability_matrix.png`: Valid empirical and theoretical operating frequency intervals.
10. `fig10_summary_comparison_chart.png`: Direct bar chart comparison at benchmark cell radius ($d = 3\text{ km}$).

---

## Testing

The repository includes a comprehensive automated test suite with **32 tests** covering units, models, simulations, and sensitivity sweeps:

```bash
python -m pytest
```

Output:
```text
============================= 32 passed in 0.72s =============================
```

---

## Reproducibility

Reproducibility is strictly enforced via:
- Fixed random seeds (`seed=42`) for all stochastic simulations.
- Deterministic YAML scenario parameter files.
- Version-pinned `requirements.txt` and `pyproject.toml`.

---

## Limitations

- **Classical Frequency Bounds:** Okumura-Hata is calibrated up to 1.5 GHz, and COST-231 up to 2.0 GHz. Extrapolating them to sub-6 GHz 5G (3.5 GHz) or mmWave (28 GHz) overestimates coverage.
- **Topographical Clutter:** Empirical models assume statistical terrain roughness rather than site-specific 3D vector geometries.
- **Small-Scale Fast Fading:** Models focus on large-scale median path loss and shadow fading; small-scale multipath fast fading (Rayleigh/Rician) is not modeled.

---

## Future Enhancements

- Implementation of 3GPP TR 38.901 3D channel models for 5G/6G sub-6 GHz and mmWave.
- Integration with GIS / OpenStreetMap building footprints for 3D ray-tracing.
- Machine-learning-based channel prediction using Graph Neural Networks (GNNs).

---

## Project Team

- **Harsh Yadav** (Reg No: `RA2311003011546`)
- **Utkarsh Dabas** (Reg No: `RA2311003011550`)
- **Tamanna Singh** (Reg No: `RA2311003011570`)

*Department of Electronics & Communication Engineering / Telecommunications*  
*Capstone Evaluation & Research Defense — Academic Year 2025–2026*


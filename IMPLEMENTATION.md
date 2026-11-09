# IMPLEMENTATION GUIDE
## Comparative Analysis of Wireless Signal Propagation Models

**Project Title:** Comparative Analysis of Wireless Signal Propagation Models  
**Project Team:**  
- Harsh Yadav (`RA2311003011546`)
- Utkarsh Dabas (`RA2311003011550`)
- Tamanna Singh (`RA2311003011570`)  
**Department:** Electronics & Communication Engineering  
**Academic Year:** 2025–2026  
**Software Version:** 1.0.0  
**Repository Architecture:** Production-Grade Scientific Python Package  

---

## 1. Overview and Engineering Architecture

This document provides a comprehensive technical walkthrough of the software implementation, modules, mathematical logic, testing suite, and reproducibility mechanics of the `wireless-propagation-analysis` framework.

### 1.1 Source Code Tree
```text
Wireless/
├── pyproject.toml                     # PEP 518/621 Build & dependency configuration
├── requirements.txt                   # Fixed runtime and development dependencies
├── README.md                          # Main GitHub repository documentation
├── IMPLEMENTATION.md                  # Complete implementation architecture reference
├── app.py                             # Interactive Streamlit dashboard
├── experiments/
│   └── scenarios/
│       ├── rural.yaml                 # Scenario A: 900 MHz rural macrocell
│       ├── urban.yaml                 # Scenario B: 1800 MHz urban macrocell
│       ├── suburban.yaml              # Scenario C: 1800 MHz suburban macrocell
│       ├── indoor.yaml                # Scenario D: 2.4 GHz indoor WLAN / small cell
│       └── 5g_midband.yaml            # Scenario E: 3.5 GHz 5G mid-band microcell
├── scripts/
│   ├── run_simulation.py              # CLI for executing scenario distance/frequency sweeps
│   ├── generate_figures.py            # Batch generator for all 10 scientific figures
│   ├── generate_report.py             # Generates hard-copy academic PDF report
│   ├── generate_presentation.py       # Generates 15-slide PowerPoint deck (.pptx)
│   └── create_notebooks.py            # Regenerates the 4 Jupyter notebooks
├── notebooks/
│   ├── 01_model_exploration.ipynb     # Interactive introduction to each model
│   ├── 02_model_comparison.ipynb      # Direct multi-model comparison sweeps
│   ├── 03_sensitivity_analysis.ipynb  # Height, frequency, and exponent sensitivity
│   └── 04_final_results.ipynb         # Publication-grade results and summary tables
├── src/
│   └── propagation/
│       ├── __init__.py                # Package version and namespace exports
│       ├── core/
│       │   ├── __init__.py            # Core exports
│       │   ├── exceptions.py          # Custom error hierarchy & ModelRangeWarning
│       │   ├── units.py               # Vectorized unit conversions (Hz, m, W, dBm)
│       │   └── link_budget.py         # RF link budget & fade margin calculations
│       ├── models/
│       │   ├── __init__.py            # Model registry exports
│       │   ├── base.py                # PropagationModel abstract base class
│       │   ├── free_space.py          # Friis Free Space Path Loss model
│       │   ├── two_ray.py             # Two-Ray Ground Reflection (exact + asymptotic)
│       │   ├── log_distance.py        # Log-Distance Path Loss model
│       │   ├── okumura.py             # Okumura model with Tokyo empirical fits
│       │   ├── hata.py                # Okumura-Hata model (urban, suburban, rural)
│       │   ├── cost231.py             # COST-231 Hata model for 1.5 - 2.0 GHz
│       │   └── shadowing.py           # Log-Normal Shadowing & outage probability
│       ├── simulation/
│       │   ├── __init__.py            # Simulation exports
│       │   ├── scenario.py            # YAML configuration loader and ScenarioConfig
│       │   └── engine.py              # SimulationEngine distance & frequency sweeps
│       ├── analysis/
│       │   ├── __init__.py            # Analysis exports
│       │   ├── comparator.py          # Pairwise differences, statistics, taxonomy
│       │   └── sensitivity.py         # Antenna height and 2D parameter space sweeps
│       └── visualization/
│           ├── __init__.py            # Visualizer exports
│           └── plotting.py            # Publication-grade Matplotlib / Seaborn styling
├── tests/
│   ├── test_core.py                   # 9 unit tests for units, wavelength, link budget
│   ├── test_models.py                 # 17 unit tests for all 7 propagation models
│   ├── test_simulation.py             # 3 integration tests for scenarios & sweep engine
│   └── test_analysis.py               # 3 tests for comparator, difference & sensitivity
├── outputs/
│   ├── figures/                       # 10 generated PNG figures (300 DPI)
│   ├── reports/                       # Generated CSV datasets and PDF report
│   └── presentation/                  # Generated PowerPoint presentation (.pptx)
└── docs/
    ├── PROJECT_PLAN.md                # Phase 0 architectural plan & design choices
    ├── PROJECT_REPORT.md              # Formal academic paper report
    ├── METHODOLOGY.md                 # Mathematical derivations & theoretical equations
    ├── MODEL_REFERENCE.md             # Parameter definitions & boundary reference
    └── RESULTS.md                     # Detailed numerical findings & discussion
```

---

## 2. Core Modules and Implementation Details

### 2.1 Unit Conversion & Physical Constants (`src/propagation/core/units.py`)
- Standardizes all internal physics calculations into SI base units:
  - Distance: meters ($m$)
  - Frequency: Hertz ($Hz$)
  - Power: Watts ($W$) / decibel-milliwatts ($dBm$)
- Physical speed of light: $c = 299,792,458\text{ m/s}$.
- Provides fully vectorized bidirectional conversion functions:
  - `to_hz(freq, unit)` / `from_hz(freq_hz, unit)`
  - `to_meters(dist, unit)` / `from_meters(dist_m, unit)`
  - `watts_to_dbm(w)` / `dbm_to_watts(dbm)`
  - `mw_to_dbm(mw)` / `dbm_to_mw(dbm)`
  - `wavelength(freq, unit)`

### 2.2 RF Link Budget Engine (`src/propagation/core/link_budget.py`)
- Solves the standard RF link budget equation:
  $$P_r (\text{dBm}) = P_t (\text{dBm}) + G_t (\text{dBi}) + G_r (\text{dBi}) - PL (\text{dB}) - L_{\text{sys}} (\text{dB})$$
- Computes Effective Isotropic Radiated Power (EIRP):
  $$\text{EIRP} (\text{dBm}) = P_t (\text{dBm}) + G_t (\text{dBi})$$
- Computes Fade Margin relative to receiver sensitivity threshold:
  $$\text{Fade Margin} (\text{dB}) = P_r (\text{dBm}) - P_{\text{sensitivity}} (\text{dBm})$$

### 2.3 Abstract Base Class (`src/propagation/models/base.py`)
Every propagation model extends `PropagationModel`, which enforces:
- `calculate_path_loss(distance, frequency, distance_unit, frequency_unit, strict, **kwargs)`
- `calculate_received_power(...)`
- `validate_parameters(...)`
- `get_valid_range()`
- `get_model_name()`, `get_classification()`, `get_description()`

If input parameters fall outside a model's empirical calibration range, the framework emits a `ModelRangeWarning` (or raises `InvalidParameterError` if `strict=True`).

### 2.4 The Seven Implemented Models
1. **`FreeSpacePathLoss`:** Unobstructed line-of-sight Friis formulation ($n=2$).
2. **`TwoRayGroundReflection`:** Supports `'exact'` field superposition, `'asymptotic'` $d^{-4}$ falloff, and `'hybrid'` modes, with explicit crossover distance computation ($d_c = 4\pi h_t h_r / \lambda$).
3. **`LogDistancePathLoss`:** Parametric model supporting pre-calibrated environment presets (`urban`, `suburban`, `rural`, `indoor_los`, `indoor_obstructed`).
4. **`OkumuraModel`:** Parameterized Tokyo empirical curves ($f \in [150, 1920]$ MHz, $d \in [1, 100]$ km) with base and mobile antenna height corrections and terrain area gains.
5. **`HataModel`:** Standard closed-form Okumura-Hata equations for medium city, large city, suburban, and rural environments up to 1.5 GHz.
6. **`COST231HataModel`:** European PCS/cellular extension for 1.5 GHz to 2.0 GHz with metropolitan center correction $C_M = 3$ dB.
7. **`LogNormalShadowing`:** Stochastic large-scale fading model supporting fixed random seeds, Monte Carlo trajectory generation, 95% confidence intervals, and analytical outage probability computation via the complementary error function ($\text{erfc}$).

---

## 3. Installation and Setup Instructions

### 3.1 Prerequisites
- Python 3.11 or 3.12
- Git

### 3.2 Installation
```bash
# Clone repository
git clone https://github.com/your-username/wireless-propagation-analysis.git
cd wireless-propagation-analysis

# Create and activate virtual environment (optional but recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies and editable package
pip install -r requirements.txt
pip install -e .
```

---

## 4. Execution Commands

### 4.1 Running the Automated Test Suite
```bash
python -m pytest
```
*Executes all 32 unit and integration tests across core conversions, models, simulations, and sensitivity sweeps.*

### 4.2 Running Simulations via CLI
```bash
# Run a specific scenario
python scripts/run_simulation.py --scenario urban
python scripts/run_simulation.py --scenario rural
python scripts/run_simulation.py --scenario indoor
python scripts/run_simulation.py --scenario suburban
python scripts/run_simulation.py --scenario 5g_midband

# Run all scenarios in batch
python scripts/run_simulation.py --scenario all
```

### 4.3 Generating Figures
```bash
python scripts/generate_figures.py
```
*Outputs 10 high-resolution figures (300 DPI) into `outputs/figures/`.*

### 4.4 Generating the Hard-Copy PDF Report
```bash
python scripts/generate_report.py
```
*Generates publication-quality PDF report `outputs/reports/Wireless_Propagation_Comparative_Report.pdf`.*

### 4.5 Generating the PowerPoint Presentation
```bash
python scripts/generate_presentation.py
```
*Builds a 15-slide academic presentation `outputs/presentation/Wireless_Propagation_Analysis.pptx` embedding actual generated figures.*

### 4.6 Launching the Interactive Web Dashboard
```bash
streamlit run app.py
```
*Launches an interactive browser GUI to adjust frequency, distance range, transmit power, antenna heights, and environments in real time.*


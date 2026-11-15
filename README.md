# Comparative Analysis of Wireless Signal Propagation Models
### Classical VHF/UHF Cellular (2G–4G) to 5G New Radio & 6G mmWave / Sub-THz (0.5–100 GHz)

[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/tests-45%20passed-brightgreen.svg)]()
[![Code Style](https://img.shields.io/badge/code%20style-pep8-green.svg)]()
[![3GPP Spec](https://img.shields.io/badge/3GPP-TR%2038.901%20Rel--19-blue)]()
[![IEEE Access](https://img.shields.io/badge/IEEE%20Access-2026.3741615-red)]()

A comprehensive, scientific, and reproducible Python simulation framework for evaluating, comparing, and analyzing wireless signal propagation models across diverse carrier frequencies (150 MHz to 100 GHz), distances (1 meter to 100 kilometers), antenna configurations, and propagation environments (urban macro, street canyon, indoor office, suburban, and rural).

---

## Overview

In modern telecommunications, accurate prediction of path loss and received signal power is the bedrock of RF network dimensioning, link budget closure, beamforming array design, and cell planning.

This repository provides an end-to-end research platform implementing **13 propagation models** spanning theoretical baselines, classical empirical models, modern 3GPP standards, and cutting-edge 2026 statistical mmWave research:
- **Theoretical Models:** Friis Free Space Path Loss (FSPL), Two-Ray Ground Reflection
- **Classical Empirical Models:** Log-Distance Path Loss, Okumura Model, Okumura-Hata Model, COST-231 Hata Model
- **Stochastic Fading Models:** Log-Normal Shadow Fading (with Monte Carlo simulation and analytical outage probability)
- **5G / 6G Standards (3GPP TR 38.901 Rel 16–19):** Urban Micro (UMi) Street Canyon (LoS/NLoS), Urban Macro (UMa) (LoS/NLoS), Indoor Hotspot (InH) Office (LoS/NLoS)
- **Millimeter-Wave Reference Models:** Close-In (CI) Free-Space Reference Distance Model, Frequency-Dependent CIF Variant, Floating-Intercept / ABG Model
- **Stochastic State Transitions (IEEE Access 2026):** Probabilistic LoS–NLoS state transition channel model capturing building corner turns and shadowing dynamics

---

## Why Classical Models Fail at GHz, mmWave & Sub-THz

1. **Strict Calibration Ceilings:**
   - **Okumura-Hata** is empirically calibrated strictly between **150 MHz and 1500 MHz**.
   - **COST-231 Hata** extends Hata only up to **2000 MHz (2.0 GHz)**.
   - When extrapolated to 5G C-Band (3.5 GHz), FR3 (13 GHz), or mmWave (28 GHz / 39 GHz / 73 GHz), classical equations yield errors of 30 to 60 dB, severely miscalculating required transmitter EIRP.
2. **Breakpoints and Diffraction Inadequacies:**
   - At high frequencies ($\lambda \le 1\text{ cm}$), electromagnetic waves exhibit optical-like propagation. Knife-edge building diffraction loss exceeds 25–40 dB, causing a stark discontinuity between Line-of-Sight (LoS) and Non-Line-of-Sight (NLoS) propagation paths. Classical models aggregate clutter into an average exponent, failing to model the dual-slope roll-off separated by the physical breakpoint distance $d'_{BP}$.
3. **Atmospheric Absorption & Resonance:**
   - Classical models neglect gaseous atmospheric attenuation. At millimeter wavelengths, molecular oxygen ($O_2$) resonance creates a sharp absorption peak (~15 dB/km) around 60 GHz, while water vapor attenuation increases above 22 GHz.
4. **Physically Grounded 1-Meter Reference (CI):**
   - The Close-In (CI) free-space reference model anchors path loss at 1 meter to fundamental Maxwell physics ($FSPL(1\text{m}) = 20\log_{10}(4\pi f / c)$), providing unmatched parameter stability across non-contiguous bands compared to arbitrary empirical polynomials.

---

## Models Implemented

| Model | Classification | Complexity | Environment | Calibrated Freq | Calibrated Dist | Key Formula / Characteristics |
|---|---|---|---|---|---|---|
| **Free Space (Friis)** | Theoretical | $\mathcal{O}(1)$ Closed-form | Unobstructed LOS | Broadband | Far-field ($d > 0$) | $PL = 20\log_{10}(d) + 20\log_{10}(f) + 32.44$ |
| **Two-Ray Ground Reflection** | Theoretical | $\mathcal{O}(1)$ Vector / Asymp | Flat earth, waterways | 1 MHz – 60 GHz | 1 m – 100 km | $PL = 40\log_{10}(d) - 20\log_{10}(h_t) - 20\log_{10}(h_r)$ (for $d > d_c$) |
| **Log-Distance Path Loss** | Empirical | $\mathcal{O}(1)$ Parametric | In-building, microcell | Calibrated | $d \ge d_0$ | $PL(d) = PL(d_0) + 10 n \log_{10}(d / d_0)$ |
| **Okumura Model** | Empirical | $\mathcal{O}(1)$ Empirical Fit | Urban/Suburban macro | 150 – 1920 MHz | 1 – 100 km | Graphical Tokyo measurementsnomogram |
| **Okumura-Hata Model** | Empirical | $\mathcal{O}(1)$ Analytical | Urban, suburban, rural | 150 – 1500 MHz | 1 – 20 km | Closed-form cellular standard (2G/3G) |
| **COST-231 Hata Model** | Empirical | $\mathcal{O}(1)$ Analytical | Urban & metropolitan | 1500 – 2000 MHz | 1 – 20 km | Extended Hata for 1.8–2.0 GHz PCS |
| **Log-Normal Shadowing** | Stochastic | $\mathcal{O}(N)$ Monte Carlo | Cluttered terrain | All bands | $d \ge d_0$ | $PL = \overline{PL}(d) + X_\sigma, \; X_\sigma \sim \mathcal{N}(0, \sigma^2)$ |
| **3GPP TR 38.901 UMi** | Standard (Rel 16–19) | $\mathcal{O}(1)$ Dual-Slope | Street Canyon (Micro) | 0.5 – 100 GHz | 10 m – 5 km | Dual-slope with breakpoint $d'_{BP}$, LoS/NLoS states |
| **3GPP TR 38.901 UMa** | Standard (Rel 16–19) | $\mathcal{O}(1)$ Dual-Slope | Urban Macrocell | 0.5 – 100 GHz | 10 m – 5 km | Macro BS ($h_{BS}=25\text{ m}$), user height scaling |
| **3GPP TR 38.901 InH** | Standard (Rel 16–19) | $\mathcal{O}(1)$ Analytical | Indoor Mixed Office | 0.5 – 100 GHz | 1 m – 150 m | Indoor office small-cell propagation |
| **Close-In (CI) Model** | Empirical mmWave | $\mathcal{O}(1)$ 1-m Anchor | mmWave / Sub-THz | 0.5 – 100 GHz | 1 m – 5 km | $PL = FSPL(1\text{m}) + 10 n \log_{10}(d) + X_\sigma$ |
| **Floating-Intercept (ABG)**| Empirical mmWave | $\mathcal{O}(1)$ 3-Parameter | Multi-band 5G/6G | 0.5 – 100 GHz | 1 m – 5 km | $PL = 10\alpha\log_{10}(d) + \beta + 10\gamma\log_{10}(f) + X_\sigma$ |
| **LoS–NLoS Transition** | Stochastic Transition| $\mathcal{O}(N)$ Bernoulli Draws| Urban Street Canyon | 0.5 – 100 GHz | 10 m – 5 km | Probabilistic mixture $P_{LoS}(d)PL_{LoS} + (1-P_{LoS})PL_{NLoS}$ |

---

## Mathematical Formulations

### 1. 3GPP TR 38.901 Urban Micro (UMi) Street Canyon
- **Breakpoint Distance:**
  $$d'_{BP} = \frac{4 h'_{BS} h'_{UT} f_c}{c}, \quad h'_{BS} = h_{BS} - 1.0\text{ m}, \quad h'_{UT} = h_{UT} - 1.0\text{ m}$$
- **Line-of-Sight (LoS):**
  $$PL_1 = 32.4 + 21.0\log_{10}(d_{3D}) + 20.0\log_{10}(f_c) \quad \text{for } 10\text{ m} \le d_{2D} \le d'_{BP}$$
  $$PL_2 = 32.4 + 40.0\log_{10}(d_{3D}) + 20.0\log_{10}(f_c) - 9.5\log_{10}\left((d'_{BP})^2 + (h_{BS} - h_{UT})^2\right) \quad \text{for } d'_{BP} < d_{2D} \le 5000\text{ m}$$
  $$\sigma_{SF} = 4.0\text{ dB}$$
- **Non-Line-of-Sight (NLoS):**
  $$PL'_{NLoS} = 35.3\log_{10}(d_{3D}) + 22.4 + 21.3\log_{10}(f_c) - 0.3(h_{UT} - 1.5)$$
  $$PL_{NLoS} = \max(PL_{LoS}, PL'_{NLoS}), \quad \sigma_{SF} = 7.82\text{ dB}$$
- **LoS Probability:**
  $$P_{LoS}(d_{2D}) = \begin{cases} 1.0 & d_{2D} \le 18\text{ m} \\ \frac{18}{d_{2D}} + \exp\left(-\frac{d_{2D}}{36}\right)\left(1 - \frac{18}{d_{2D}}\right) & d_{2D} > 18\text{ m} \end{cases}$$

### 2. 3GPP TR 38.901 Urban Macro (UMa)
- **LoS:**
  $$PL_1 = 28.0 + 22.0\log_{10}(d_{3D}) + 20.0\log_{10}(f_c)$$
  $$PL_2 = 28.0 + 40.0\log_{10}(d_{3D}) + 20.0\log_{10}(f_c) - 9.5\log_{10}\left((d'_{BP})^2 + (h_{BS} - h_{UT})^2\right)$$
- **NLoS:**
  $$PL'_{NLoS} = 13.54 + 39.08\log_{10}(d_{3D}) + 20.0\log_{10}(f_c) - 0.6(h_{UT} - 1.5)$$
  $$PL_{NLoS} = \max(PL_{LoS}, PL'_{NLoS}), \quad \sigma_{SF} = 6.0\text{ dB}$$

### 3. 3GPP TR 38.901 Indoor Hotspot (InH Office)
- **LoS:** $PL = 32.4 + 17.3\log_{10}(d_{3D}) + 20.0\log_{10}(f_c), \quad \sigma_{SF} = 3.0\text{ dB}$
- **NLoS:** $PL = \max\left(PL_{LoS}, 38.3\log_{10}(d_{3D}) + 17.30 + 24.9\log_{10}(f_c)\right), \quad \sigma_{SF} = 8.03\text{ dB}$

### 4. Close-In (CI) and CIF Models
- **Standard CI:**
  $$PL_{CI}(f, d) = FSPL(f, 1\text{m}) + 10 n \log_{10}(d) + X_\sigma, \quad FSPL(f, 1\text{m}) = 20\log_{10}\left(\frac{4\pi f}{c}\right)$$
  *Presets: UMi LoS ($n=2.1, \sigma=4.0\text{ dB}$), UMi NLoS ($n=3.19, \sigma=8.2\text{ dB}$).*
- **CIF (Frequency-Dependent Exponent):**
  $$n(f) = n\left(1 + b \frac{f - f_0}{f_0}\right), \quad PL_{CIF}(f, d) = FSPL(f, 1\text{m}) + 10 n(f) \log_{10}(d) + X_\sigma$$

### 5. Floating-Intercept (ABG) Model
$$PL_{ABG}(f, d) = 10\alpha\log_{10}(d) + \beta + 10\gamma\log_{10}(f_c) + X_\sigma$$
*Standard UMi Preset:* $\alpha = 3.53$, $\beta = 22.4$, $\gamma = 2.13$, $\sigma = 7.82\text{ dB}$. Includes ordinary least squares (OLS) parameter fitter `fit_from_data`.

### 6. LoS–NLoS State Transition Model (IEEE Access 2026)
Models stochastic beam tracking transitions as user terminals turn street corners:
$$PL_{\text{mean}}(d) = P_{LoS}(d) PL_{LoS}(d) + (1 - P_{LoS}(d)) PL_{NLoS}(d)$$
$$S \sim \text{Bernoulli}(P_{LoS}(d)), \quad PL_{\text{realized}}(d) = \begin{cases} PL_{LoS}(d) + X_{\sigma, LoS} & S = 1 \\ PL_{NLoS}(d) + X_{\sigma, NLoS} & S = 0 \end{cases}$$

---

## Scenarios (YAML Configurations)

The repository provides 9 scenario configuration files in `experiments/scenarios/`:
1. `urban.yaml`: 1800 MHz LTE Urban Macrocell benchmark ($h_t = 30\text{ m}, h_r = 1.5\text{ m}$, 1–10 km).
2. `suburban.yaml`: 900 MHz Suburban deployment ($h_t = 30\text{ m}$, 1–10 km).
3. `rural.yaml`: 450 MHz Rural open terrain coverage ($h_t = 50\text{ m}$, 1–20 km).
4. `indoor.yaml`: 2.4 GHz Indoor Wi-Fi obstructed environment ($d = 1\text{ m to }100\text{ m}$).
5. `5g_midband.yaml`: 3.5 GHz 5G C-band microcellular deployment.
6. `5g_midband_3500mhz.yaml`: 3.5 GHz 5G NR microcell using 3GPP TR 38.901 and Close-In models.
7. `fr3_upper_midband_13ghz.yaml`: 13 GHz FR3 (7–24 GHz) upper mid-band bridging 5G and 6G.
8. `mmwave_28ghz.yaml`: 28 GHz mmWave Street Canyon with LoS–NLoS state transitions.
9. `sub_thz_6g_100ghz.yaml`: 100 GHz Sub-THz extreme capacity small cell ($d = 5\text{ m to }500\text{ m}$).

---

## Multi-Frequency Benchmark Summary

Generated by `python scripts/generate_benchmarks.py` and exported to `outputs/reports/benchmark_summary_table.csv`:

| Model | 1.8 GHz (1 km) | 3.5 GHz (1 km) | 13 GHz (1 km) | 28 GHz (100 m) | 28 GHz (200 m) | 28 GHz (1 km) |
|---|---|---|---|---|---|---|
| **Free Space (Friis)** | 97.6 dB | 103.3 dB | 114.7 dB | 101.4 dB | 107.4 dB | 121.4 dB |
| **Two-Ray Ground Reflection** | 95.2 dB | 101.0 dB | 112.4 dB | 111.8 dB | 104.5 dB | 157.0 dB |
| **Log-Distance ($n=3.0$)** | 127.6 dB | 133.3 dB | 144.7 dB | 121.4 dB | 130.4 dB | 151.4 dB |
| **Okumura-Hata** | 134.3 dB | *OOR (>1.5 GHz)* | *OOR (>1.5 GHz)* | *OOR (>1.5 GHz)* | *OOR (>1.5 GHz)* | *OOR (>1.5 GHz)* |
| **COST-231 Hata** | 136.2 dB | *OOR (>2.0 GHz)* | *OOR (>2.0 GHz)* | *OOR (>2.0 GHz)* | *OOR (>2.0 GHz)* | *OOR (>2.0 GHz)* |
| **3GPP TR 38.901 UMi LoS** | 100.4 dB | 106.2 dB | 117.6 dB | **103.4 dB** | 109.7 dB | 124.3 dB |
| **3GPP TR 38.901 UMi NLoS** | 120.7 dB | 126.6 dB | 138.8 dB | **123.9 dB** | 134.5 dB | 159.1 dB |
| **3GPP TR 38.901 UMa LoS** | 99.0 dB | 104.8 dB | 116.2 dB | 101.2 dB | 107.6 dB | 122.9 dB |
| **3GPP TR 38.901 UMa NLoS** | 115.8 dB | 121.7 dB | 133.2 dB | 121.1 dB | 132.5 dB | 159.7 dB |
| **Close-In (CI) ($n=3.19$)** | 121.2 dB | 127.0 dB | 138.4 dB | **125.2 dB** | 134.8 dB | 157.1 dB |
| **Floating-Intercept (ABG)** | 120.7 dB | 126.6 dB | 138.8 dB | 123.8 dB | 134.5 dB | 159.1 dB |
| **LoS–NLoS Transition Mean** | 116.8 dB | 122.7 dB | 134.8 dB | **119.1 dB** | 132.1 dB | 158.5 dB |

*Hand-checked test vectors at 28 GHz, $d = 100\text{ m}$: FSPL(1m) = 61.4 dB, UMi LoS = 103.3 dB, UMi NLoS = 123.8 dB, CI = 125.2 dB (all matching within 0.1 dB tolerance).*

---

## Publication Figures

All 14 scientific figures are generated at **300 DPI** in `outputs/figures/`:
1. `fig01_path_loss_vs_distance.png`: Comparative path loss across all models on log distance scale.
2. `fig02_received_power_vs_distance.png`: Received power with link margin and -100 dBm threshold.
3. `fig03_path_loss_vs_frequency.png`: Carrier frequency sensitivity from 150 MHz to 3.5 GHz.
4. `fig04_environmental_comparison.png`: Urban Large, Urban Medium, Suburban, and Rural terrain curves.
5. `fig05_model_difference_vs_baseline.png`: Excess path loss discrepancy relative to Free Space.
6. `fig06_shadowing_distribution.png`: Log-normal Monte Carlo trajectories and Gaussian probability density function.
7. `fig07_antenna_height_sensitivity.png`: Impact of transmitter height $h_t$ (20–200 m) and receiver height $h_r$ (1–10 m).
8. `fig08_path_loss_2d_heatmap.png`: 2D parameter space heatmap of path loss over distance and frequency.
9. `fig09_model_applicability_matrix.png`: Standardized operating frequency intervals (0.5 to 100 GHz).
10. `fig10_summary_comparison_chart.png`: Direct bar chart comparison at benchmark cell radius ($d = 3\text{ km}$).
11. `fig11_mmwave_vs_classical_28ghz.png`: Classical vs 3GPP UMi LoS/NLoS vs CI vs ABG at 28 GHz.
12. `fig12_broadband_pl_vs_frequency.png`: Broadband sweep from 0.5 to 100 GHz highlighting Hata ($\le 1.5\text{ GHz}$) and COST-231 ($\le 2\text{ GHz}$) validity limits.
13. `fig13_los_probability_and_mixture.png`: LoS probability decay curve and stochastic LoS–NLoS state transition realizations (IEEE Access 2026).
14. `fig14_benchmark_barchart_3_5ghz_and_28ghz.png`: Grouped benchmark comparison at 3.5 GHz and 28 GHz.

---

## How to Run

### 1. Run Automated Test Suite (pytest)
```bash
python -m pytest
```
*Executes all 45 unit and integration tests including hand-checked vectors, monotonicity, bounds, CIF scaling, OLS fitting, and boundary warnings.*

### 2. Generate Publication Figures (300 DPI)
```bash
python scripts/generate_figures.py
```

### 3. Generate Multi-Frequency Benchmark Table (CSV)
```bash
python scripts/generate_benchmarks.py
```

### 4. Generate Hard-Copy Research Report (PDF)
```bash
python scripts/generate_report.py
```
*Outputs `outputs/reports/Wireless_Propagation_Comparative_Report.pdf`.*

### 5. Launch Interactive Streamlit Dashboard
```bash
streamlit run app.py
```

### 6. Run MATLAB Dual-Band Simulation
Open `path_loss_simulation.m` in MATLAB or GNU Octave:
```matlab
run('path_loss_simulation.m')
```

---

## References

1. **3GPP TR 38.901 (V17.0.0 & Rel-19):**  
   *3rd Generation Partnership Project; Technical Specification Group Radio Access Network; Study on channel model for frequencies from 0.5 to 100 GHz (Release 19 update).*
2. **Poddar et al. (2025):**  
   *Overview of 3GPP Release 19 Study on Channel Modeling Enhancements to TR 38.901 for 6G.*  
   arXiv:2507.19266 [eess.SP].
3. **Inam Ullah, Hesham El-Sayed, Alexis A. Dowhuszko, Jyri Hämäläinen (2026):**  
   *Statistical Path Loss Modeling of LoS–NLoS Transitions for mmWave Communications in Urban Environments.*  
   **IEEE Access**, 2026. DOI: [10.1109/ACCESS.2026.3741615](https://doi.org/10.1109/ACCESS.2026.3741615).
4. **Sun, Rappaport, Thomas et al. (2016):**  
   *Investigation of Prediction Accuracy, Sensitivity, and Parameter Stability of Large-Scale Propagation Path Loss Models for 5G Wireless Communications.*  
   **IEEE Transactions on Antennas and Propagation**, arXiv:1603.04404.

---

## Future Work

- **Indoor Factory (InF) & Rural Macro (RMa):** Integrating specialized 3GPP clutter scenarios for Industrial IoT and broad-area coverage.
- **Sub-THz Above 100 GHz:** Extending frequency bounds into D-band (130–175 GHz) and G-band (220–330 GHz) incorporating enhanced molecular absorption profiles.
- **Ray-Tracing & ML Predictions:** Physics-informed neural networks (PINNs) and Graph Neural Networks (GNNs) trained on LiDAR 3D point-cloud city environments.

---

## Project Team

- **Harsh Yadav** (Reg No: `RA2311003011546`)
- **Utkarsh Dabas** (Reg No: `RA2311003011550`)
- **Tamanna Singh** (Reg No: `RA2311003011570`)

*Department of Electronics & Communication Engineering / Computing Technologies*  
*SRM Institute of Science and Technology, Kattankulathur*  
*Course: 21CSE458T — Wireless and Mobile Communication | Academic Year 2025–2026*

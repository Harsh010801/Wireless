# PROJECT PLAN & ARCHITECTURAL SPECIFICATION
## Comparative Analysis of Wireless Signal Propagation Models

**Project Title:** Comparative Analysis of Wireless Signal Propagation Models  
**Domain:** Wireless Communications, Propagation Modeling, Numerical Simulation, Comparative Sensitivity Analysis  
**Repository Architecture:** Standard Modular Python Package with Automated Testing, CLI, Jupyter Notebooks, Academic PPT Generator, and Interactive Dashboard  
**Status:** In Progress (Phase 0 Complete)

---

## 1. Project Objective & Scope

The primary objective is to design, develop, rigorously validate, and present a scientific simulation and comparative analysis framework that investigates wireless signal propagation across diverse frequency bands (150 MHz to 5 GHz), transmission distances (1 m to 100 km), antenna configurations (heights and gains), and environments (urban, suburban, rural/open, indoor).

### Key Research Questions Addressed:
1. **Model Hierarchy:** Under which conditions do theoretical models (Free Space, Two-Ray) diverge from empirical formulations (Okumura, Hata, COST-231)?
2. **Distance Sensitivity:** How does the path loss exponent ($n \in [1.6, 6.0]$) transition across environments, and where is the critical two-ray crossover distance $d_c$?
3. **Frequency Sensitivity:** What is the quantitative impact of carrier frequency scaling from UHF cellular bands (900 MHz, 1800 MHz) to sub-6 GHz 5G bands (3.5 GHz)?
4. **Environmental Corrections:** How do urban clutter, building penetration, and rural terrain corrections alter median path attenuation?
5. **Applicability Bounds:** Where do empirical models break down or yield scientifically invalid extrapolations, and how should a resilient framework report boundary warnings?
6. **Stochastic Variability:** How does log-normal shadow fading ($X_\sigma \sim \mathcal{N}(0, \sigma^2)$) induce coverage margins and outage risks in practical link budgets?

---

## 2. Model Taxonomy and Mathematical Formulations

| Model Name | Classification | Domain / Validity Range | Key Parameters | Primary Equations |
|---|---|---|---|---|
| **Free Space Path Loss (FSPL)** | Theoretical / Deterministic LOS | Unobstructed line-of-sight, all frequencies, $d > 0$ | $d$ (m), $f$ (Hz) | $PL_{FS}(d) = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}(4\pi/c)$ |
| **Two-Ray Ground Reflection** | Theoretical / Multipath | Flat earth, ground reflection, $d > 0$, $h_t, h_r > 0$ | $d$, $f$, $h_t$, $h_r$, $\Gamma$ | Exact: $\left\|\frac{e^{-jk d_1}}{d_1} + \Gamma \frac{e^{-jk d_2}}{d_2}\right\|^{-2}$; Asymptotic: $40\log_{10}(d) - 20\log_{10}(h_t) - 20\log_{10}(h_r)$ |
| **Log-Distance Path Loss** | Empirical / Parametric | Indoor/Outdoor macro/microcell, $d \ge d_0$ | $d_0$, $PL(d_0)$, exponent $n$ | $PL(d) = PL(d_0) + 10 n \log_{10}(d / d_0)$ |
| **Okumura Model** | Empirical (Classical) | Tokyo terrain, $f \in [150, 1920]\text{ MHz}$, $d \in [1, 100]\text{ km}$, $h_t \in [30, 1000]\text{ m}$, $h_r \in [1, 10]\text{ m}$ | $f, d, h_t, h_r$, Environment | $PL(d) = L_{FS}(f, d) + A_{mu}(f, d) - G(h_{te}) - G(h_{re}) - G_{AREA}$ |
| **Hata Model** | Empirical (Okumura Closed-Form) | $f \in [150, 1500]\text{ MHz}$, $d \in [1, 20]\text{ km}$, $h_b \in [30, 200]\text{ m}$, $h_m \in [1, 10]\text{ m}$ | $f, d, h_b, h_m$, Environment (Urban, Suburban, Rural) | $PL_{urb} = 69.55 + 26.16\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d)$ |
| **COST-231 Hata Model** | Empirical (Extended Hata) | $f \in [1500, 2000]\text{ MHz}$, $d \in [1, 20]\text{ km}$, $h_b \in [30, 200]\text{ m}$, $h_m \in [1, 10]\text{ m}$ | $f, d, h_b, h_m$, City type ($C_M$) | $PL_{COST} = 46.3 + 33.9\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d) + C_M$ |
| **Log-Normal Shadowing** | Stochastic / Large-Scale Fading | Cluttered propagation environments, $d \ge d_0$ | $d_0, n, \sigma$ (dB), seed | $PL(d) = PL(d_0) + 10 n \log_{10}(d / d_0) + X_\sigma$, where $X_\sigma \sim \mathcal{N}(0, \sigma^2)$ |

---

## 3. System Architecture

The project is structured under the `src/` directory to guarantee high modularity, testability, and reuse:

```
src/
    propagation/
        __init__.py
        core/
            units.py             # Rigorous unit conversion (Hz/MHz/GHz, m/km, W/mW/dBm)
            link_budget.py        # Link budget calculation & conversions
            exceptions.py         # Domain-specific errors & validation warnings
        models/
            __init__.py
            base.py               # Abstract base class: PropagationModel
            free_space.py         # Friis / FSPL model
            two_ray.py            # Two-ray ground reflection (exact + asymptotic)
            log_distance.py       # Log-distance path loss model
            okumura.py            # Okumura model with empirical curves & bounds
            hata.py               # Okumura-Hata model (urban, suburban, rural)
            cost231.py            # COST-231 Hata model
            shadowing.py          # Log-normal shadowing (reproducible seed)
        simulation/
            __init__.py
            scenario.py           # Scenario definition and YAML parsing
            engine.py             # Multi-model sweep engine (distance & frequency)
        analysis/
            __init__.py
            comparator.py         # Pairwise differences, percentage divergence, statistics
            sensitivity.py        # Parameter sensitivity sweeps (height, frequency, exponent)
        visualization/
            __init__.py
            plotting.py           # Publication-quality matplotlib/seaborn generation
```

---

## 4. Input Parameters and Strict Unit Convention

To avoid unit ambiguity (a common trap in propagation calculations):
- **Base SI Units internally:**
  - Distance: meters ($m$)
  - Frequency: Hertz ($Hz$)
  - Power: Watts ($W$) / Decibel-milliwatts ($dBm$)
- **Flexible external user inputs:**
  - Distance helper: `Distance(value, unit="km"|"m")`
  - Frequency helper: `Frequency(value, unit="MHz"|"GHz"|"Hz")`
  - Power helper: `Power(value, unit="dBm"|"W"|"mW")`
- Models internally convert to their required canonical empirical units (e.g., Hata takes $f$ in MHz and $d$ in km) and perform strict boundary checks.

---

## 5. Planned Scenarios and Controlled Experiments

### Predefined Scenarios:
1. **Scenario A (Rural):** $f = 900\text{ MHz}$, $d \in [0.1, 20]\text{ km}$, Rural/Open
2. **Scenario B (Urban):** $f = 1800\text{ MHz}$, $d \in [0.1, 10]\text{ km}$, Urban medium/large
3. **Scenario C (Suburban):** $f = 1800\text{ MHz}$, $d \in [0.1, 15]\text{ km}$, Suburban
4. **Scenario D (Indoor):** $f = 2.4\text{ GHz}$, $d \in [1, 100]\text{ m}$, Indoor obstructed/LOS
5. **Scenario E (5G Mid-Band / Higher Frequency):** $f = 3.5\text{ GHz}$, $d \in [0.05, 5]\text{ km}$, Urban microcell analysis

### Controlled Experiments (Outputs saved in `outputs/figures/`):
- **Exp 1:** Path Loss vs Distance across all applicable models
- **Exp 2:** Received Power vs Distance with link budget parameters ($P_t, G_t, G_r, L_{sys}$)
- **Exp 3:** Frequency Sensitivity Analysis (sweeping 150 MHz to 3.5 GHz)
- **Exp 4:** Distance Sensitivity & Model Divergence
- **Exp 5:** Environmental Comparison (Rural vs Suburban vs Urban vs Indoor)
- **Exp 6:** Antenna Height Sensitivity (Base station $h_b \in [20, 200]\text{ m}$, Mobile $h_m \in [1, 10]\text{ m}$)
- **Exp 7:** Log-Normal Shadowing Realizations, Confidence Bounds ($\pm 1.96\sigma$), and Outage Probability
- **Exp 8:** Model Discrepancy & Difference Matrix ($\Delta PL_{A,B}$)
- **Exp 9:** 2D Parameter Heatmap (Path loss over Distance vs Frequency)
- **Exp 10:** Model Validity Range and Applicability Map

---

## 6. Execution Roadmap & Verification Milestones

1. **Phase 1: Repository Setup** -> Create directory hierarchy, `pyproject.toml`, `requirements.txt`, `.gitignore`.
2. **Phase 2: Mathematical Core** -> Implement `units.py`, `link_budget.py`, `exceptions.py` + write unit tests.
3. **Phase 3: Propagation Models** -> Implement all 7 models adhering to `PropagationModel` abstract interface + tests.
4. **Phase 4: Simulation Engine** -> Scenario loading, parameter sweeps, vectorized calculations, YAML scenarios.
5. **Phase 5: Analysis Module** -> Summary tables, model metrics, discrepancy calculations, sensitivity analysis.
6. **Phase 6: Visualization System** -> Scientific figures with grids, units, professional formatting, saved to `outputs/figures/`.
7. **Phase 7: Jupyter Notebooks** -> 4 dedicated research notebooks (`01` to `04`) executing the core engine.
8. **Phase 8: Comprehensive Documentation & Hard Copy Report** -> `README.md`, `PROJECT_REPORT.md`, `METHODOLOGY.md`, `MODEL_REFERENCE.md`, `RESULTS.md`, `IMPLEMENTATION.md`, and PDF generator for printable hard copy.
9. **Phase 9: Academic Presentation (PPT)** -> Python-pptx generation with actual generated simulation graphs and structured 15 slides.
10. **Phase 10: Interactive Streamlit Dashboard** -> `app.py` for dynamic web-based parameter tuning and scenario inspection.
11. **Phase 11: Final Quality Assurance** -> Full test suite run, verification checklist, end-to-end smoke tests.


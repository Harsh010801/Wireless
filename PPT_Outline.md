# PRESENTATION SLIDE-BY-SLIDE OUTLINE (15 SLIDES)

## Project Title
**Comparative Analysis of Wireless Signal Propagation Models (Free Space, Okumura and Hata) using MATLAB & Python**

### Course & Institutional Information
- **Course Code:** 21CSE458T — Wireless and Mobile Communication
- **Program:** B.Tech Computer Science and Engineering (7th Semester)
- **Institution:** Department of Computer Science and Engineering

### Project Team Members
1. **Harsh Yadav** — `RA2311003011546`
2. **Utkarsh Dabas** — `RA2311003011550`
3. **Tamanna Singh** — `RA2311003011570`

---

## Slide 1: Title & Project Overview
- **Title:** Comparative Analysis of Wireless Signal Propagation Models
- **Subtitle:** A Numerical & Empirical Evaluation of Free Space, Okumura, and Hata Models
- **Course:** 21CSE458T — Wireless and Mobile Communication
- **Team Presenters:**
  - Harsh Yadav (`RA2311003011546`)
  - Utkarsh Dabas (`RA2311003011550`)
  - Tamanna Singh (`RA2311003011570`)
- **Key Message:** Evaluation of theoretical vs. empirical propagation models to understand wireless path loss, attenuation scaling, and cellular link budgeting.

---

## Slide 2: Introduction & Motivation
- **What is Path Loss?**
  - Reduction in power density (attenuation) as an electromagnetic radio wave propagates through space.
  - Expressed logarithmically in decibels (dB): $PL(d) = 10 \log_{10}(P_t / P_r)$.
- **Why Propagation Models Matter:**
  - Essential for cellular dimensioning, base station placement, transmitter EIRP determination, and handover boundary mapping.
  - Underestimating loss causes dead zones and dropped calls; overestimating causes excessive co-channel interference and inflated capital expenditure (CAPEX).
- **Core Research Question:**
  - How drastically do empirical obstacles (buildings, terrain, clutter) deviate signal decay from the idealized inverse-square law?

---

## Slide 3: Theoretical Foundation — Free Space Path Loss (FSPL)
- **Concept:**
  - Based on the Friis transmission formula for isotropic radiation in an unobstructed, vacuum-like line-of-sight (LOS) medium.
- **Governing Mathematical Equation:**
  $$L_{\text{FSPL}}(\text{dB}) = 20\log_{10}(d) + 20\log_{10}(f) + 32.44$$
  *(where $d$ is in kilometers, $f$ is in megahertz)*
- **Key Characteristics:**
  - Path loss exponent $n = 2$ (loss grows strictly at $20\text{ dB/decade}$).
  - Strictly lower bound; ignores reflection, diffraction, scattering, atmospheric absorption, and ground terrain.

---

## Slide 4: Empirical Foundation — Okumura Propagation Model
- **Historical Background:**
  - Developed by Yoshihisa Okumura et al. (1968) from extensive field measurements in Tokyo, Japan.
  - Graphical/nomogram-based model widely considered the pioneer of cellular network planning.
- **Open Area Correction Formulation:**
  - For open, rural areas free of tall obstacles, standard empirical correction applies:
  $$K_{\text{open}} = -4.78(\log_{10}(f))^2 + 18.33\log_{10}(f) - 40.94$$
  $$L_{\text{Okumura}} = L_{\text{Hata}} + K_{\text{open}}$$
- **Significance:**
  - Incorporates terrain roughness and environment-specific correction factors.

---

## Slide 5: Empirical Foundation — Hata Urban Model
- **Standardization & Formulaic Representation:**
  - Formulated by Masaharu Hata (1980) to convert Okumura's graphical curves into closed-form parametric equations.
- **Mathematical Formulations:**
  - Mobile Antenna Correction Factor (Small/Medium City):
    $$a(h_{re}) = (1.1\log_{10}(f) - 0.7)h_{re} - (1.56\log_{10}(f) - 0.8)$$
  - Base Urban Attenuation Formula:
    $$L_{\text{Hata}}(\text{dB}) = 69.55 + 26.16\log_{10}(f) - 13.82\log_{10}(h_{te}) - a(h_{re}) + [44.9 - 6.55\log_{10}(h_{te})]\log_{10}(d)$$
- **Effective Exponent:**
  - For $h_{te} = 30\text{ m}$, distance attenuation coefficient is $44.9 - 6.55\log_{10}(30) \approx 35.22\text{ dB/decade}$ ($n \approx 3.52$).

---

## Slide 6: Simulation Parameters & Experimental Setup
- **Standard Benchmark Configurations:**
  - Carrier Frequency ($f$): **$900\text{ MHz}$** (GSM-900 / Cellular Band)
  - Base Station Antenna Height ($h_{te}$): **$30\text{ m}$** (Macro-cellular Tower)
  - Mobile Station Antenna Height ($h_{re}$): **$1.5\text{ m}$** (Handheld User Equipment)
  - Distance Range ($d$): **$1\text{ km}$ to $20\text{ km}$** (Macrocell coverage span)
  - Step Resolution: $1\text{ km}$ discrete intervals for tabulations, dense grid for curves.
- **Evaluation Criteria:**
  - Path loss magnitude (dB), rate of decay (dB/km and dB/decade), and comparative divergence.

---

## Slide 7: Simulation Methodology & Implementation Architecture
- **Dual Software Framework:**
  - **Python 3 Engine:** High-performance vectorized numerical computation via NumPy and plotting via Matplotlib (`path_loss_simulation.py`).
  - **MATLAB Engine:** Matrix-based engineering implementation (`path_loss_simulation.m`).
- **Reproducible Pipeline:**
  1. Input parameter validation against model domains.
  2. Mobile antenna height correction factor computation ($a(h_{re})$).
  3. Vectorized distance-dependent path loss evaluation across $d \in [1, 20]\text{ km}$.
  4. Formatted console output table generation.
  5. Publication-quality chart rendering and export (`path_loss_graph.png`).

---

## Slide 8: Quantitative Simulation Results (Table)
- **Exact Numerical Readings Generated:**

| Distance $d$ (km) | Free Space Path Loss (dB) | Okumura (Open Area) (dB) | Hata (Urban Area) (dB) |
|---|---|---|---|
| **1.0 km** | **91.52** | **97.90** | **126.40** |
| 2.0 km | 97.54 | 108.51 | 137.00 |
| 4.0 km | 103.56 | 119.11 | 147.61 |
| 6.0 km | 107.09 | 125.31 | 153.81 |
| 8.0 km | 109.58 | 129.71 | 158.21 |
| 10.0 km | 111.52 | 133.12 | 161.62 |
| 12.0 km | 113.11 | 135.91 | 164.40 |
| 14.0 km | 114.44 | 138.26 | 166.76 |
| 16.0 km | 115.60 | 140.30 | 168.80 |
| 18.0 km | 116.63 | 142.10 | 170.59 |
| **20.0 km** | **117.55** | **143.73** | **172.23** |

---

## Slide 9: Visual Comparative Graph (`path_loss_graph.png`)
- **Graph Description:**
  - Plot title: *Path Loss vs Distance (f=900 MHz)*
  - X-axis: Distance (km) from 1 to 20 km
  - Y-axis: Path Loss (dB) from 80 to 180 dB
  - Legend & Styles:
    - **Blue dash-dot curve (`o` markers):** Free Space Path Loss
    - **Green dashed curve (`s` markers):** Okumura (Open Area)
    - **Red solid curve (`^` markers):** Hata (Urban Model)
- **Key Visual Insight:**
  - The three curves diverge increasingly with distance due to differing logarithmic slope coefficients ($20\text{ dB/decade}$ vs $35.22\text{ dB/decade}$).

---

## Slide 10: Comparative Analysis & Model Divergence
- **Divergence at $1\text{ km}$:**
  - Hata vs Free Space: $126.40 - 91.52 = \mathbf{34.88\text{ dB}}$ penalty.
  - Okumura vs Free Space: $97.90 - 91.52 = \mathbf{6.38\text{ dB}}$ penalty.
- **Divergence at $20\text{ km}$:**
  - Hata vs Free Space: $172.23 - 117.55 = \mathbf{54.68\text{ dB}}$ penalty ($>290,000\times$ more signal attenuation in linear scale!).
  - Okumura vs Free Space: $143.73 - 117.55 = \mathbf{26.18\text{ dB}}$ penalty.
- **Takeaway:**
  - Obstacles, buildings, and multipath scattering introduce profound additional losses that theoretical LOS equations completely overlook.

---

## Slide 11: Environmental Clutter & Physical Mechanisms
- **Why Free Space is Overly Optimistic:**
  - Assumes a sterile environment with infinite clearance around the first Fresnel zone.
  - In real terrestrial deployments, signals encounter ground reflections, shadowing, building penetration losses, and atmospheric attenuation.
- **Urban Morphology Effects in Hata:**
  - High building density blocks LOS rays, creating multipath propagation dominated by diffraction over rooftops and street-canyon scattering.
- **Open Area Behavior in Okumura:**
  - Trees and natural undulations cause moderate attenuation beyond free space, but far less than man-made concrete structures ($28.5\text{ dB}$ lower loss than urban Hata).

---

## Slide 12: Cellular Network Planning & Engineering Implications
- **Link Budget Calculations:**
  - Given $P_t = +43\text{ dBm}$ ($20\text{ W}$ base station) and receiver sensitivity $P_{r,\min} = -104\text{ dBm}$:
  - Maximum allowable path loss: $MAPL \approx 147\text{ dB}$.
  - Under Free Space: Coverage exceeds $20\text{ km}$ easily.
  - Under Hata Urban: Maximum cell radius is limited to approximately **$4\text{ km}$**!
- **CAPEX and Base Station Density:**
  - Realistic modeling using Hata mandates deploying multiple base stations with frequency reuse to eliminate coverage holes.

---

## Slide 13: Model Limitations & Operating Ranges
- **Free Space Model:**
  - Limited strictly to outer-space satellite links or line-of-sight microwave links with cleared Fresnel zones.
- **Hata Urban Model Bounds:**
  - Carrier Frequency: $150\text{ MHz} \le f \le 1500\text{ MHz}$
  - Base Station Height: $30\text{ m} \le h_{te} \le 200\text{ m}$
  - Mobile Station Height: $1\text{ m} \le h_{re} \le 10\text{ m}$
  - Distance: $1\text{ km} \le d \le 20\text{ km}$
  - *Limitation:* Inapplicable to microcells ($d < 1\text{ km}$) or modern cellular bands above $2\text{ GHz}$.

---

## Slide 14: Future Scope & Advanced Extensions
- **5G/6G High-Frequency Bands:**
  - Extending models to mmWave ($28\text{ GHz}, 39\text{ GHz}$) and Sub-THz frequencies where atmospheric absorption and rain fade dominate.
- **3GPP TR 38.901 & Modern Standards:**
  - Implementing 3GPP Urban Micro (UMi), Urban Macro (UMa), and Indoor Office (InH) stochastic path loss models.
- **Machine Learning & Ray Tracing:**
  - Incorporating 3D LiDAR/GIS building data with deterministic 3D ray-tracing simulations and deep learning path-loss predictors.

---

## Slide 15: Conclusion & Academic References
- **Summary Conclusion:**
  - **Free Space** provides theoretical lower bound but severely underestimates terrestrial loss.
  - **Okumura (Open)** accurately models rural/suburban scenarios with moderate clutter.
  - **Hata (Urban)** provides the most realistic, standardized benchmark for macrocellular urban link budgeting.
- **Key Academic References:**
  1. T. S. Rappaport, *Wireless Communications: Principles and Practice*, 2nd ed., Prentice Hall, 2002.
  2. Y. Okumura et al., "Field strength and its variability in VHF and UHF land-mobile radio service," *Rev. Elec. Commun. Lab.*, vol. 16, no. 9–10, pp. 825–873, 1968.
  3. M. Hata, "Empirical formula for propagation loss in land mobile radio services," *IEEE Trans. Veh. Technol.*, vol. 29, no. 3, pp. 317–325, Aug. 1980.

---
*Thank you! Questions and Discussion welcomed.*


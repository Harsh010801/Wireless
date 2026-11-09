# ACADEMIC RESEARCH REPORT
## Comparative Analysis of Wireless Signal Propagation Models

**Project Team:**  
- Harsh Yadav (`RA2311003011546`)
- Utkarsh Dabas (`RA2311003011550`)
- Tamanna Singh (`RA2311003011570`)  
**Affiliation:** Department of Electronics & Communication Engineering / Telecommunications  
**Academic Year:** 2025–2026  
**Repository:** `wireless-propagation-analysis`  
**License:** MIT  

---

## Abstract

Accurate prediction of radio frequency (RF) path loss and received signal power is fundamental to the dimensioning, coverage planning, and interference management of modern wireless networks. This study presents a rigorous computational and theoretical comparative analysis of seven prominent wireless signal propagation models: Free Space Path Loss (Friis), Two-Ray Ground Reflection, Log-Distance Path Loss, Okumura Model, Okumura-Hata Model, COST-231 Hata Model, and Log-Normal Shadowing. Implemented in a modular, vectorized Python simulation engine, these models were systematically evaluated across standard cellular and wireless scenarios spanning 150 MHz to 3.5 GHz and distances from 1 meter to 20 kilometers under urban, suburban, rural, and indoor environments. The findings reveal that theoretical line-of-sight models underestimate urban terrestrial propagation loss by up to 55 dB, two-ray multipath induces an asymptotic $d^{-4}$ roll-off beyond the crossover distance $d_c$, and log-normal shadow fading demands an empirical fade margin of 12–16 dB for 95% cell-edge reliability. This paper delineates the mathematical foundations, parameter bounds, computational complexity, and practical limitations of each model to guide wireless systems engineering.

---

## 1. Introduction & Background

Wireless communication channels represent one of the most hostile and dynamic transmission media in electrical engineering. As electromagnetic waves propagate from a transmitting antenna toward a mobile receiver, they encounter reflection from planar surfaces, diffraction over building edges, diffuse scattering from rough textures, and clutter absorption from buildings and foliage.

In wireless network planning, engineers cannot conduct drive tests for every conceivable base station location. Instead, they rely on mathematical propagation models to calculate the link budget, determine cell radius, position base stations, and allocate frequency channels. Selecting an inappropriate model can result in massive coverage blackspots or unmanageable co-channel interference.

---

## 2. Theoretical Framework & Implemented Models

### 2.1 Taxonomy of Propagation Models
Wireless propagation models are broadly classified into three paradigms:
1. **Theoretical / Deterministic Models:** Derived from Maxwell’s electromagnetic field equations and geometric optics (e.g. Friis Free Space, Two-Ray Ground Reflection).
2. **Empirical / Parametric Models:** Derived from statistical regression curves fitted to physical field measurements in specific cities (e.g. Okumura, Okumura-Hata, COST-231).
3. **Stochastic Models:** Capturing spatial variations and shadow fading via probability distributions (e.g. Log-Normal Shadowing).

### 2.2 Mathematical Specifications
Detailed specifications and derivations are cataloged in [`docs/METHODOLOGY.md`](METHODOLOGY.md) and [`docs/MODEL_REFERENCE.md`](MODEL_REFERENCE.md).

---

## 3. Simulation System Architecture

The software architecture is engineered under `src/propagation/` following strict object-oriented principles, type hints, and full NumPy array vectorization:
- `core/`: Unit conversion utilities (`units.py`), RF link budget engine (`link_budget.py`), and error/warning hierarchies (`exceptions.py`).
- `models/`: Concrete implementations of all seven propagation models inheriting from the abstract base class `PropagationModel`.
- `simulation/`: Scenario parser (`scenario.py`) and simulation engine (`engine.py`) managing distance sweeps, frequency sweeps, and reproducibility.
- `analysis/`: Comparative metrics (`comparator.py`) and sensitivity sweeps (`sensitivity.py`).
- `visualization/`: Publication-grade plotting system (`plotting.py`).

---

## 4. Controlled Experimental Results

### 4.1 Path Loss and Received Power vs Distance
As demonstrated in Figure 1 and Figure 2 (Urban Scenario B, 1800 MHz, $P_t = 43\text{ dBm}$, $h_t = 30\text{ m}$, $h_r = 1.5\text{ m}$):
- Free space loss increases monotonically from 77.6 dB at 100 m to 117.6 dB at 10 km (decay rate $20\text{ dB/decade}$).
- COST-231 Hata and Okumura models predict 101.0 dB to 171.4 dB across the same distance span ($35\text{ dB/decade}$).
- At a 10 km cell edge, the received power drops to $-62.6\text{ dBm}$ under Free Space, but drops severely to $-116.4\text{ dBm}$ under COST-231 Hata, falling well below the $-100\text{ dBm}$ receiver sensitivity threshold.

### 4.2 Two-Ray Ground Reflection Crossover Dynamics
The two-ray model illustrates the physical transition between free space and destructive earth reflection:
$$d_c = \frac{4\pi h_t h_r f}{c} = 3.39\text{ km} \quad (\text{at } 1800\text{ MHz})$$
At short distances ($d < d_c$), the direct and reflected rays alternate between constructive and destructive interference, producing multipath ripple. At long distances ($d > d_c$), destructive interference is permanent, steepening the path loss slope to $40\log_{10}(d)$ ($n = 4$).

### 4.3 Environmental Clutter Comparison
At 900 MHz:
- Rural / Open terrain exhibits the lowest terrestrial path loss (115.1 dB at 10 km).
- Suburban environments introduce an extra ~18 dB of loss (133.2 dB at 10 km).
- Urban Large Cities experience the highest attenuation (146.2 dB at 10 km) due to heavy concrete reflection and high street canyon diffraction.

### 4.4 Shadow Fading and Outage Probability
Under log-normal shadow fading with standard deviation $\sigma = 6-8$ dB, the received power varies substantially at identical distances from the base station. Monte Carlo simulations (1,500 iterations) verify a Gaussian distribution of path loss in dB. To guarantee an outage probability $P_{\text{outage}} \le 5\%$, the link budget must allocate a fade margin:
$$M_{\text{fade}} = Q^{-1}(0.05) \cdot \sigma = 1.645 \cdot \sigma \approx 13.2\text{ dB} \quad (\text{or } 1.96\sigma = 15.7\text{ dB for } 97.5\%)$$

---

## 5. Comparative Evaluation & Model Selection Matrix

| Model | Classification | Complexity | Environment | Valid Freq | Valid Dist | Primary Use Case | Main Limitation |
|---|---|---|---|---|---|---|---|
| **Free Space** | Theoretical | $\mathcal{O}(1)$ | Ideal LOS | All bands | Far-field | Satellite / Microwave | No terrestrial multipath |
| **Two-Ray** | Theoretical | $\mathcal{O}(1)$ | Flat Earth | 1 MHz - 60 GHz | $d > 0$ | Rural / Highways / Maritime | Unrealistic in urban clutter |
| **Log-Distance** | Empirical | $\mathcal{O}(1)$ | Configurable | Calibrated | $d \ge d_0$ | Indoor Wi-Fi / Microcells | Needs empirical exponent $n$ |
| **Okumura** | Empirical | $\mathcal{O}(1)$ | Urban/Suburban | 150 - 1920 MHz | 1 - 100 km | Macrocell planning | Graphical fits; $d \ge 1$ km |
| **Hata** | Empirical | $\mathcal{O}(1)$ | Macrocell | 150 - 1500 MHz | 1 - 20 km | 2G/3G Cellular GSM-900 | Max 1.5 GHz limit |
| **COST-231** | Empirical | $\mathcal{O}(1)$ | Urban PCS | 1500 - 2000 MHz | 1 - 20 km | PCS / 3G 1.8-2.0 GHz | Invalid for 5G $> 2$ GHz |
| **Shadowing** | Stochastic | $\mathcal{O}(N)$ | Clutter | All bands | $d \ge d_0$ | Outage & Link Budgets | Random realizations |

---

## 6. Practical Limitations & Future Enhancements

### 6.1 Limitations
1. **Classical Empirical Bounds:** Okumura, Hata, and COST-231 models are uncalibrated above 2 GHz. Directly using them for 5G NR mid-band (3.5 GHz) or mmWave (28 GHz) represents an out-of-domain extrapolation that overestimates coverage.
2. **Terrain Agnostic:** Empirical models assume quasi-smooth earth and statistical building averages rather than specific 3D digital elevation models (DEM).

### 6.2 Future Research Extensions
- Implementation of 3GPP TR 38.901 3D urban micro (UMi) and urban macro (UMa) models for 5G/6G sub-6 GHz and mmWave.
- GPU-accelerated shooting and bouncing ray (SBR) 3D ray tracing using OpenStreetMap GIS spatial clutter.
- Machine-learning-based channel prediction trained on drive-test data using Graph Neural Networks (GNNs).

---

## 7. Conclusion

This comparative analysis demonstrates the critical trade-offs between theoretical rigor, empirical calibration, and stochastic modeling in wireless communications. While theoretical models provide essential physical bounds, empirical and stochastic models are indispensable for realistic cellular planning. The open-source framework developed herein provides a robust, testable, and reproducible foundation for academic instruction, laboratory experimentation, and research extension.


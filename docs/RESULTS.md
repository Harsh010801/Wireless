# SCIENTIFIC RESULTS AND COMPARATIVE ANALYSIS
## Comparative Analysis of Wireless Signal Propagation Models

**Project Team:** Harsh Yadav (`RA2311003011546`), Utkarsh Dabas (`RA2311003011550`), Tamanna Singh (`RA2311003011570`)  
**Department:** Electronics & Communication Engineering / Telecommunications  
**Repository:** `wireless-propagation-analysis`  

---

## 1. Simulation Setup and Baseline Scenarios

Simulations were executed across five canonical scenarios:
- **Scenario A (Rural):** $f = 900\text{ MHz}$, $d \in [0.1, 20]\text{ km}$, $P_t = 46\text{ dBm}$, $h_t = 45\text{ m}$, $h_r = 1.5\text{ m}$
- **Scenario B (Urban):** $f = 1800\text{ MHz}$, $d \in [0.1, 10]\text{ km}$, $P_t = 43\text{ dBm}$, $h_t = 30\text{ m}$, $h_r = 1.5\text{ m}$
- **Scenario C (Suburban):** $f = 1800\text{ MHz}$, $d \in [0.1, 15]\text{ km}$, $P_t = 43\text{ dBm}$, $h_t = 35\text{ m}$, $h_r = 1.5\text{ m}$
- **Scenario D (Indoor):** $f = 2400\text{ MHz}$, $d \in [1, 100]\text{ m}$, $P_t = 20\text{ dBm}$, $h_t = 2.5\text{ m}$, $h_r = 1.0\text{ m}$
- **Scenario E (5G Mid-Band):** $f = 3500\text{ MHz}$, $d \in [0.05, 5]\text{ km}$, $P_t = 38\text{ dBm}$, $h_t = 15\text{ m}$, $h_r = 1.5\text{ m}$

---

## 2. Numerical Results Summary (Urban Scenario B, 1800 MHz)

| Model Key | Min Path Loss (dB) | Max Path Loss (dB) | Mean Path Loss (dB) | Std (dB) | Median (dB) | Min Rx Power (dBm) | Max Rx Power (dBm) |
|---|---|---|---|---|---|---|---|
| **Free Space (Friis)** | 77.6 | 117.6 | 97.6 | 11.6 | 97.6 | -62.6 | -22.6 |
| **Two-Ray Ground Refl.** | 73.1 | 127.0 | 97.8 | 14.2 | 95.2 | -72.0 | -18.1 |
| **Log-Distance ($n=3.2$)** | 101.6 | 165.6 | 133.6 | 18.6 | 133.6 | -110.6 | -46.6 |
| **Okumura Model** | 112.6 | 172.2 | 142.4 | 17.3 | 142.4 | -117.2 | -57.6 |
| **Okumura-Hata** | 99.0 | 169.5 | 134.3 | 20.4 | 134.3 | -114.5 | -44.0 |
| **COST-231 Hata** | 101.0 | 171.4 | 136.2 | 20.4 | 136.2 | -116.4 | -46.0 |
| **Log-Normal Shadowing** | 87.2 | 176.4 | 133.3 | 19.9 | 131.6 | -121.4 | -32.2 |

*(Simulation parameters: $P_t = 43\text{ dBm}$, $G_t = 15\text{ dBi}$, $G_r = 0\text{ dBi}$, $L_{\text{sys}} = 3\text{ dB}$, $\text{EIRP} = 58\text{ dBm}$)*

---

## 3. Detailed Comparative Findings

### 3.1 Model Divergence and Attenuation Severity
1. **Lowest Predicted Loss:** Free Space Path Loss yields the lowest attenuation across all distances (77.6 dB at 100 m to 117.6 dB at 10 km). It serves strictly as an unattainable theoretical lower bound for terrestrial channels.
2. **Highest Predicted Loss:** Okumura and COST-231 Hata predict the highest attenuation (reaching 171.4 - 172.2 dB at 10 km). In dense urban canyons, building diffraction and clutter absorption add an excess loss of **40 to 55 dB** above free space.
3. **COST-231 vs Hata:** At 1800 MHz, COST-231 predicts approximately **2 dB higher path loss** than the extrapolated Hata equation, reflecting the empirical correction factor tailored specifically to PCS bands.

### 3.2 Distance Dependence & Two-Ray Crossover
For the Urban Macrocell setup ($h_t = 30$ m, $h_r = 1.5$ m, $f = 1800$ MHz):
- Wavelength $\lambda = 0.1665$ m.
- Crossover distance:
  $$d_c = \frac{4\pi (30)(1.5)}{0.1665} \approx 3,391\text{ meters } (3.39\text{ km})$$
- For $d < 3.39$ km, constructive and destructive interference creates rapid spatial oscillations around the Free Space curve.
- For $d > 3.39$ km, destructive ground interference dominates, and path loss scales asymptotically as $40\log_{10}(d)$ ($n = 4$, 40 dB/decade roll-off).

### 3.3 Environmental Attenuation Hierarchy (Scenario C & A)
Evaluating Hata at $f = 900$ MHz across environments:
- **Urban Large City:** 146.2 dB at 10 km
- **Urban Medium City:** 143.1 dB at 10 km
- **Suburban:** 133.2 dB at 10 km ($\Delta \approx -10$ dB vs Urban Medium)
- **Rural / Open:** 115.1 dB at 10 km ($\Delta \approx -28$ dB vs Urban Medium)

This demonstrates that suburban clutter reduces path loss by ~10 dB due to lower building density and wider roadways, while open rural terrain provides nearly 28 dB of additional coverage reach.

### 3.4 Shadowing Outage Margins
Under log-normal shadow fading ($\sigma = 8$ dB in urban channels):
- At $d = 3$ km, mean path loss is $129.5$ dB, yielding a mean received power of $-74.5$ dBm.
- While the mean received power is well above the receiver sensitivity threshold ($-100$ dBm), location-to-location variations mean that without an adequate fade margin, mobile users behind large structures will suffer severe outages.
- To guarantee **95% cell-edge coverage reliability**, network engineers must provision an extra fade margin of:
  $$M_{\text{fade}} = 1.96 \times \sigma = 1.96 \times 8\text{ dB} = 15.68\text{ dB}$$

---

## 4. Synthesis of Answers to Master Research Questions

1. **Lowest/Highest Path Loss:** Free Space predicts the lowest; Okumura / COST-231 Hata predict the highest.
2. **Distance Scaling:** Free Space scales at $20\log_{10}(d)$ ($n=2$); Two-Ray transitions from oscillatory to $40\log_{10}(d)$ ($n=4$); empirical cellular models scale at $\sim 35\log_{10}(d)$ ($n \approx 3.5$).
3. **Frequency Sensitivity:** Path loss increases logarithmically with frequency ($20\log_{10}(f)$ to $33.9\log_{10}(f)$). Moving from 900 MHz to 3.5 GHz incurs an additional $12-16$ dB of median propagation loss.
4. **Environmental Corrections:** Urban clutter adds $28-30$ dB compared to open rural terrain, and $10-12$ dB compared to suburban environments.
5. **Model Applicability:** Theoretical models are ideal for clear LOS/highway links; empirical models (Hata, COST-231) are suited for cellular macrocells; Log-Normal Shadowing is necessary for coverage reliability and link margin planning.
6. **Model Discrepancies:** Different models diverge by up to **55 dB** under identical link parameters, underscoring the critical importance of scenario-matched model selection.
7. **Computational Complexity:** Free Space, Two-Ray, Log-Distance, and Hata are $\mathcal{O}(1)$ closed-form equations; Log-Normal Monte Carlo analysis requires $\mathcal{O}(N)$ statistical sampling.


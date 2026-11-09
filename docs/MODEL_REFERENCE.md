# MODEL REFERENCE MANUAL
## Mathematical & Implementation Reference for Propagation Models

**Author:** Harsh Yadav  
**Repository:** `wireless-propagation-analysis`  

---

## 1. Free Space Path Loss (Friis) Model
- **Class:** `FreeSpacePathLoss` (`src/propagation/models/free_space.py`)
- **Classification:** Theoretical / Deterministic
- **Core Formula:**
  $$PL(d, f) = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}\left(\frac{4\pi}{c}\right)$$
- **Assumptions:** Unobstructed line-of-sight in infinite lossless vacuum; far-field condition $d > 2D^2/\lambda$; no obstacles, multipath, atmospheric absorption, or ground reflection.
- **Valid Range:** $d > 0$, $f > 0$ (all RF bands).
- **Primary Use Case:** Satellite communications, microwave line-of-sight backhaul links, anechoic test chambers.
- **Limitation:** Severely underestimates terrestrial path loss in built or vegetated environments.

---

## 2. Two-Ray Ground Reflection Model
- **Class:** `TwoRayGroundReflection` (`src/propagation/models/two_ray.py`)
- **Classification:** Theoretical / Multipath
- **Core Formula:**
  - Exact:
    $$PL_{\text{exact}} = -10\log_{10}\left| \frac{\lambda}{4\pi d_{\text{dir}}} e^{-j k d_{\text{dir}}} + \Gamma \frac{\lambda}{4\pi d_{\text{ref}}} e^{-j k d_{\text{ref}}} \right|^2$$
  - Asymptotic:
    $$PL_{\text{asymp}} = 40\log_{10}(d) - 20\log_{10}(h_t) - 20\log_{10}(h_r)$$
- **Crossover Distance:** $d_c = \frac{4\pi h_t h_r}{\lambda}$.
- **Assumptions:** Flat planar earth with uniform specular reflection ($\Gamma \approx -1$); grazing angle $< 0.5^\circ$; $d \gg (h_t + h_r)$.
- **Valid Range:** $h_t \in [1, 500]$ m, $h_r \in [0.5, 50]$ m, $d \in [1\text{ m}, 100\text{ km}]$.
- **Primary Use Case:** Rural highways, maritime/waterway links, open desert or runway communications.
- **Limitation:** Fails in urban street canyons where irregular buildings block ground specular reflections.

---

## 3. Log-Distance Path Loss Model
- **Class:** `LogDistancePathLoss` (`src/propagation/models/log_distance.py`)
- **Classification:** Empirical / Parametric
- **Core Formula:**
  $$PL(d) = PL(d_0) + 10 n \log_{10}\left(\frac{d}{d_0}\right)$$
- **Standard Exponents ($n$):**
  - Free Space: $n = 2.0$
  - Urban Macrocell: $n = 2.7 - 3.5$
  - Suburban: $n = 2.8 - 3.0$
  - Shadowed Urban: $n = 3.0 - 5.0$
  - Indoor LOS: $n = 1.6 - 1.8$
  - Indoor Obstructed: $n = 4.0 - 6.0$
- **Valid Range:** $d \ge d_0$.
- **Primary Use Case:** In-building Wi-Fi/Bluetooth design, campus microcells, generalized empirical modeling.
- **Limitation:** Highly dependent on having empirical measurement data to select an appropriate exponent $n$.

---

## 4. Okumura Model
- **Class:** `OkumuraModel` (`src/propagation/models/okumura.py`)
- **Classification:** Empirical (Graphical Data Fit)
- **Core Formula:**
  $$PL(d, f) = L_{\text{FSL}} + A_{\text{mu}}(f, d) - G(h_{te}) - G(h_{re}) - G_{\text{AREA}}$$
- **Calibration Bounds:**
  - Carrier Frequency: $150\text{ MHz} \le f \le 1920\text{ MHz}$
  - Distance: $1\text{ km} \le d \le 100\text{ km}$
  - Base Station Height: $30\text{ m} \le h_{te} \le 1000\text{ m}$
  - Mobile Station Height: $1\text{ m} \le h_{re} \le 10\text{ m}$
- **Primary Use Case:** Classical macrocellular network planning in Japan and East Asia.
- **Limitation:** Does not provide closed-form equations originally (relies on chart interpolation); uncalibrated for distances $< 1$ km.

---

## 5. Okumura-Hata Model
- **Class:** `HataModel` (`src/propagation/models/hata.py`)
- **Classification:** Empirical (Parametric Closed-Form)
- **Core Formula:**
  $$PL_{\text{urb}} = 69.55 + 26.16\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d)$$
- **Calibration Bounds:**
  - Carrier Frequency: $150\text{ MHz} \le f \le 1500\text{ MHz}$
  - Distance: $1\text{ km} \le d \le 20\text{ km}$
  - Base Station Height: $30\text{ m} \le h_b \le 200\text{ m}$
  - Mobile Station Height: $1\text{ m} \le h_m \le 10\text{ m}$
- **Primary Use Case:** 2G GSM-900 cellular planning, VHF/UHF public safety dispatch, rural broadband.
- **Limitation:** Strict $1.5$ GHz ceiling; unusable for PCS 1900, AWS, LTE, or 5G bands.

---

## 6. COST-231 Hata Model
- **Class:** `COST231HataModel` (`src/propagation/models/cost231.py`)
- **Classification:** Empirical (Extended Analytical)
- **Core Formula:**
  $$PL_{\text{COST}} = 46.3 + 33.9\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d) + C_M$$
  where $C_M = 0$ dB (medium city/suburban) or $3$ dB (dense metropolitan).
- **Calibration Bounds:**
  - Carrier Frequency: $1500\text{ MHz} \le f \le 2000\text{ MHz}$
  - Distance: $1\text{ km} \le d \le 20\text{ km}$
  - Base Station Height: $30\text{ m} \le h_b \le 200\text{ m}$
  - Mobile Station Height: $1\text{ m} \le h_m \le 10\text{ m}$
- **Primary Use Case:** DCS-1800, GSM-1900, 3G UMTS-2100 macrocellular network planning.
- **Limitation:** Invalid above $2$ GHz; cannot model sub-6 GHz 5G (3.5 GHz) or mmWave.

---

## 7. Log-Normal Shadowing Model
- **Class:** `LogNormalShadowing` (`src/propagation/models/shadowing.py`)
- **Classification:** Stochastic (Large-Scale Shadow Fading)
- **Core Formula:**
  $$PL(d) = PL(d_0) + 10 n \log_{10}\left(\frac{d}{d_0}\right) + X_\sigma, \quad X_\sigma \sim \mathcal{N}(0, \sigma^2)$$
- **Analytical Metrics:**
  - 95% Confidence Bounds: $\overline{PL}(d) \pm 1.96\sigma$
  - Outage Probability: $P_{\text{outage}} = Q\left(\frac{\overline{P}_r - \gamma_{\text{th}}}{\sigma}\right) = \frac{1}{2}\text{erfc}\left(\frac{\overline{P}_r - \gamma_{\text{th}}}{\sqrt{2}\sigma}\right)$
- **Primary Use Case:** Link margin dimensioning, coverage reliability analysis, Monte Carlo network planning.
- **Limitation:** Does not model small-scale multipath fast fading (Rayleigh/Rician); requires statistical averaging over tens of wavelengths.


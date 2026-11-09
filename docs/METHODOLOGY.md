# RESEARCH METHODOLOGY
## Comparative Analysis of Wireless Signal Propagation Models

**Project Team:** Harsh Yadav (`RA2311003011546`), Utkarsh Dabas (`RA2311003011550`), Tamanna Singh (`RA2311003011570`)  
**Department:** Electronics & Communication Engineering / Telecommunications  
**Repository:** `wireless-propagation-analysis`  

---

## 1. Research Overview & Theoretical Foundations

Radio frequency (RF) signal propagation through the terrestrial atmosphere and built environments is fundamentally governed by electromagnetic wave theory (Maxwell’s equations) coupled with complex boundary interactions—reflection, diffraction, scattering, and atmospheric absorption. 

To model these physical phenomena in wireless systems engineering, researchers and network planners utilize three primary classes of models:
1. **Theoretical / Deterministic Models:** Derived directly from physical laws (e.g., Friis Free Space, Two-Ray Ground Reflection).
2. **Empirical / Parametric Models:** Derived from extensive statistical regressions of physical field measurements across defined geographical environments (e.g., Okumura, Okumura-Hata, COST-231 Hata).
3. **Stochastic Models:** Superimposing probabilistic distributions (e.g., Log-Normal Shadowing) to account for random spatial clutter variations and calculate outage probabilities.

---

## 2. Mathematical Formulations & Derivations

### 2.1 Free Space Path Loss (Friis Formulation)
Assuming an ideal isotropic radiator emitting power $P_t$ in an unbounded, lossless medium:
$$\text{Power Density } S = \frac{P_t G_t}{4\pi d^2} \quad (\text{W/m}^2)$$
The effective aperture of an isotropic receiver antenna is:
$$A_e = \frac{\lambda^2}{4\pi} = \frac{c^2}{4\pi f^2}$$
Thus, the received power ratio is:
$$\frac{P_r}{P_t} = G_t G_r \left(\frac{\lambda}{4\pi d}\right)^2 = G_t G_r \left(\frac{c}{4\pi d f}\right)^2$$
Defining Path Loss $PL = P_t G_t G_r / P_r$ in decibels:
$$PL_{\text{FS}}(d, f) = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}\left(\frac{4\pi}{c}\right)$$
Using SI units ($d$ in meters, $f$ in Hz, $c = 299,792,458$ m/s):
$$20\log_{10}\left(\frac{4\pi}{c}\right) \approx -147.5522\text{ dB}$$
When distance is expressed in kilometers ($d_{\text{km}}$) and frequency in megahertz ($f_{\text{MHz}}$):
$$PL_{\text{FS}}(d, f) = 20\log_{10}(d_{\text{km}}) + 20\log_{10}(f_{\text{MHz}}) + 32.448\text{ dB}$$

---

### 2.2 Two-Ray Ground Reflection Model
In line-of-sight terrestrial links where the receiver is positioned above the earth, the received electric field is a vector superposition of two components:
1. Direct LOS ray traversing distance $d_{\text{dir}} = \sqrt{d^2 + (h_t - h_r)^2}$
2. Specular ground-reflected ray traversing distance $d_{\text{ref}} = \sqrt{d^2 + (h_t + h_r)^2}$ with complex reflection coefficient $\Gamma$.

Phase difference between the rays:
$$\Delta \phi = \frac{2\pi}{\lambda}(d_{\text{ref}} - d_{\text{dir}})$$
For small grazing angles over typical soil, $\Gamma \approx -1$. For distances $d \gg (h_t + h_r)$:
$$\Delta d \approx \frac{2 h_t h_r}{d}, \quad \Delta \phi \approx \frac{4\pi h_t h_r}{\lambda d}$$
Superposition of field strengths gives the asymptotic power ratio:
$$\frac{P_r}{P_t} \approx G_t G_r \frac{h_t^2 h_r^2}{d^4}$$
$$PL_{\text{Two-Ray, Asymptotic}}(d) = 40\log_{10}(d) - 20\log_{10}(h_t) - 20\log_{10}(h_r)$$
Notice that in the asymptotic far-field region ($d > d_c$), path loss:
1. Increases at **40 dB per decade** (decay exponent $n = 4$).
2. Is **independent of carrier frequency**.
3. Decreases by **6 dB for every doubling of antenna height**.

The crossover distance $d_c$ marking the boundary between interference oscillations and monotonic $d^{-4}$ decay is:
$$d_c = \frac{4\pi h_t h_r}{\lambda} = \frac{4\pi h_t h_r f}{c}$$

---

### 2.3 Log-Distance Path Loss Model
Captures generic attenuation across indoor and outdoor channels via empirical path-loss exponent $n$:
$$PL(d) = PL(d_0) + 10 n \log_{10}\left(\frac{d}{d_0}\right)$$
Where $d_0$ is a close-in reference distance ($1\text{ m}$ indoor, $100\text{ m}-1000\text{ m}$ outdoor macrocell), and $PL(d_0)$ is typically computed via free-space Friis.

---

### 2.4 Okumura Empirical Model
Formulated by Yoshihisa Okumura from extensive drive measurements in Tokyo:
$$PL_{\text{Okumura}}(d, f) = L_{\text{FSL}}(f, d) + A_{\text{mu}}(f, d) - G(h_{te}) - G(h_{re}) - G_{\text{AREA}}$$
Where:
- $L_{\text{FSL}}$: Free space path loss.
- $A_{\text{mu}}(f, d)$: Median attenuation relative to free space in urban quasi-smooth terrain ($h_{te}=200$ m, $h_{re}=3$ m).
- Base station height gain: $G(h_{te}) = 20\log_{10}(h_{te}/200)$ for $30 \le h_{te} \le 1000$ m.
- Mobile height gain: $G(h_{re}) = 10\log_{10}(h_{re}/3)$ for $h_{re} \le 3$ m, and $20\log_{10}(h_{re}/3)$ for $3 < h_{re} \le 10$ m.
- Environment gain $G_{\text{AREA}}$: $0$ dB (urban), suburban, or rural/open correction.

---

### 2.5 Okumura-Hata Model
Closed-form analytical equations parameterized by Hata (1980):
$$PL_{\text{urban}}(d, f) = 69.55 + 26.16\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d)$$
Mobile antenna correction $a(h_m)$ in medium city:
$$a(h_m) = (1.1\log_{10}(f) - 0.7)h_m - (1.56\log_{10}(f) - 0.8)$$
Suburban correction:
$$PL_{\text{suburban}} = PL_{\text{urban}} - 2\left[\log_{10}\left(\frac{f}{28}\right)\right]^2 - 5.4$$
Rural/open correction:
$$PL_{\text{rural}} = PL_{\text{urban}} - 4.78[\log_{10}(f)]^2 + 18.33\log_{10}(f) - 40.94$$

---

### 2.6 COST-231 Hata Model
Extends Hata into PCS and 3G frequency allocations ($1500\text{ MHz} \le f \le 2000\text{ MHz}$):
$$PL_{\text{COST231}} = 46.3 + 33.9\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + [44.9 - 6.55\log_{10}(h_b)]\log_{10}(d) + C_M$$
Where $C_M = 0$ dB for medium cities/suburban, and $C_M = 3$ dB for metropolitan dense urban centers.

---

### 2.7 Log-Normal Shadowing & Outage Probability
Stochastic shadow fading accounts for clutter obstruction:
$$PL(d) = \overline{PL}(d) + X_\sigma, \quad X_\sigma \sim \mathcal{N}(0, \sigma^2)$$
Received signal power is normally distributed: $P_r(d) \sim \mathcal{N}(\overline{P}_r(d), \sigma^2)$.

The **Outage Probability** (probability that received signal power falls below receiver threshold $\gamma_{\text{th}}$):
$$P_{\text{outage}} = P(P_r < \gamma_{\text{th}}) = \frac{1}{\sqrt{2\pi}\sigma} \int_{-\infty}^{\gamma_{\text{th}}} \exp\left(-\frac{(p - \overline{P}_r)^2}{2\sigma^2}\right) dp$$
$$P_{\text{outage}} = Q\left(\frac{\overline{P}_r - \gamma_{\text{th}}}{\sigma}\right) = \frac{1}{2} \text{erfc}\left(\frac{\overline{P}_r - \gamma_{\text{th}}}{\sqrt{2}\sigma}\right)$$

---

## 3. Link Budget Implementation

The total received power $P_r$ is derived via the radio link equation:
$$P_r (\text{dBm}) = P_t (\text{dBm}) + G_t (\text{dBi}) + G_r (\text{dBi}) - PL (\text{dB}) - L_{\text{sys}} (\text{dB})$$
- Transmit power $P_t$ in Watts is converted to dBm: $P_t(\text{dBm}) = 10\log_{10}(P_t(\text{W}) \times 1000)$.
- Effective Isotropic Radiated Power (EIRP): $\text{EIRP}(\text{dBm}) = P_t(\text{dBm}) + G_t(\text{dBi}) - L_{\text{cable}}(\text{dB})$.
- Fade Margin: $\text{FM}(\text{dB}) = P_r(\text{dBm}) - P_{\text{sensitivity}}(\text{dBm})$.

---

## 4. Software Architecture & Verification Strategy

The simulation engine is built upon an object-oriented, vectorized NumPy architecture:
1. `PropagationModel` abstract base class enforcing standard calculation signatures.
2. Parameter validation with warning flags for empirical bound exceedances.
3. YAML scenario loading for fully reproducible experimental execution.
4. Pytest test suite covering unit conversions, numerical accuracy, boundary conditions, and reproducibility.


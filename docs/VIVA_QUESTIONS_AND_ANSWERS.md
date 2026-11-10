# VIVA & ORAL DEFENSE PREPARATION GUIDE
## Comparative Analysis of Wireless Signal Propagation Models

**Project Team:**
1. **Harsh Yadav** (`RA2311003011546`)
2. **Utkarsh Dabas** (`RA2311003011550`)
3. **Tamanna Singh** (`RA2311003011570`)

**Department:** Electronics & Communication Engineering / Telecommunications  
**Academic Year:** 2025–2026  

---

### Q1. What is the fundamental difference between theoretical, empirical, and stochastic propagation models?
- **Theoretical Models (e.g., Friis Free Space, Two-Ray Ground Reflection):** Derived directly from fundamental electromagnetic laws (Maxwell's equations and geometric ray optics). They do not require tuning parameters, but assume simplified idealized geometries (e.g., vacuum or perfectly planar earth).
- **Empirical Models (e.g., Okumura, Okumura-Hata, COST-231):** Derived from statistical regressions fitted to thousands of physical drive-test measurements in specific cities. They capture complex real-world clutter and diffraction, but are strictly valid only within their calibrated frequency and distance ranges.
- **Stochastic Models (e.g., Log-Normal Shadowing):** Treat the received signal or path loss as a random variable to model spatial clutter variations (building shadowing, trees) and calculate link outage probabilities.

---

### Q2. Why does the Two-Ray Ground Reflection model decay at $40\text{ dB/decade}$ ($d^{-4}$) instead of $20\text{ dB/decade}$ ($d^{-2}$)?
In the Two-Ray model, the receiver picks up both a direct line-of-sight ray and a specular ground-reflected ray.
- At large distances ($d \gg h_t + h_r$), the path length difference $\Delta d \approx \frac{2 h_t h_r}{d}$ becomes very small compared to the wavelength.
- Because the ground reflection coefficient $\Gamma \approx -1$ for small grazing angles, the direct and reflected electric fields are nearly $180^\circ$ out of phase.
- Subtracting two almost identical field vectors yields a resulting field strength proportional to $\frac{1}{d^2}$, which means received power $P_r \propto |E|^2 \propto \frac{1}{d^4}$.
- In decibels, $10\log_{10}(d^{-4}) = -40\log_{10}(d)$, which corresponds to a steep **40 dB per decade** roll-off.

---

### Q3. What is the physical significance of the Two-Ray crossover distance $d_c$?
$$d_c = \frac{4\pi h_t h_r}{\lambda} = \frac{4\pi h_t h_r f}{c}$$
- **For $d < d_c$:** The phase difference $\Delta \phi$ between direct and reflected rays is large enough to produce alternating constructive and destructive interference ripples around the Free Space line.
- **For $d > d_c$:** Destructive phase cancellation dominates permanently, and signal power rolls off monotonically at $d^{-4}$ (40 dB/decade).
- **Frequency Dependence:** Higher carrier frequencies have shorter wavelengths $\lambda$, pushing the crossover distance $d_c$ further out into the cell.

---

### Q4. What is the key difference between Okumura and Okumura-Hata models?
- **Okumura (1968):** Based on extensive measurements conducted in Tokyo. It presented path loss as a series of graphical curves and charts for median attenuation $A_{\text{mu}}(f, d)$, base station height gain $G(h_{te})$, and mobile height gain $G(h_{re})$. It did not provide closed-form formulas, making computer automation difficult.
- **Hata (1980):** Hata fitted analytical parametric equations to Okumura's graphical curves, creating the famous closed-form Okumura-Hata formula for urban, suburban, and rural environments up to 1.5 GHz.

---

### Q5. Why was the COST-231 Hata model developed?
The original Hata model was capped at $1500\text{ MHz}$. With the advent of 2G DCS-1800, GSM-1900, and 3G PCS networks operating in the $1800-2000\text{ MHz}$ range, the European Cooperative for Scientific and Technical Research (COST) committee extended Hata’s equations up to $2000\text{ MHz}$ and added a metropolitan clutter correction factor $C_M = 3\text{ dB}$.

---

### Q6. What is Log-Normal Shadowing and why is it called "Log-Normal"?
- **Shadowing (Slow Fading):** Caused by large obstacles (buildings, hills, dense foliage) that block the main signal path between base station and mobile terminal.
- **Why Log-Normal?** The received power measured in milliwatts or Watts is log-normally distributed. When converted to decibels (logarithmic scale), the distribution becomes a standard Gaussian (Normal) distribution:
  $$PL(d) = \overline{PL}(d) + X_\sigma, \quad X_\sigma \sim \mathcal{N}(0, \sigma^2)$$
  Where $\sigma$ is the standard deviation in dB (typically $4-12\text{ dB}$).

---

### Q7. How do you calculate the required Fade Margin for 95% coverage reliability?
Since shadow fading in dB follows a zero-mean normal distribution with standard deviation $\sigma$:
- To ensure the received signal exceeds the receiver sensitivity threshold 95% of the time, the link budget must allocate a fade margin of:
  $$M_{\text{fade}} = z \times \sigma = 1.645 \times \sigma \quad (\text{for one-tailed 95\%})$$
  $$M_{\text{fade}} = 1.96 \times \sigma \quad (\text{for two-tailed 95\% / 97.5\% reliability})$$
- For a typical urban environment where $\sigma = 8\text{ dB}$, the required margin is:
  $$1.96 \times 8\text{ dB} = 15.68\text{ dB}$$

---

### Q8. What is the difference between Large-Scale Path Loss and Small-Scale Fading?
- **Large-Scale Fading (Covered in this project):** Characterizes signal attenuation over large distances (hundreds of meters to kilometers) due to distance decay and shadow fading from large obstacles. It determines cell coverage radius and base station placement.
- **Small-Scale Fading:** Characterizes rapid fluctuations of signal amplitude and phase over fractions of a wavelength (centimeters) due to multipath constructive/destructive interference. Modeled via Rayleigh or Rician statistical distributions.

---

### Q9. Why can't we use the Hata or COST-231 model for 5G at 3.5 GHz or 28 GHz mmWave?
1. **Out of Calibrated Range:** Hata is valid only up to 1.5 GHz, and COST-231 up to 2.0 GHz.
2. **Physical Inaccuracies:** At 3.5 GHz and 28 GHz, diffraction around building corners drops sharply, atmospheric absorption increases, and penetration loss through modern low-E glass reaches 25–40 dB.
3. **Microcell Geometries:** Modern 5G uses street-level microcells with base station antenna heights $h_b < 15\text{ m}$ and cell radii $d < 500\text{ m}$, violating Hata's calibration bounds ($h_b \ge 30\text{ m}$, $d \ge 1\text{ km}$). Modern 5G designs require **3GPP TR 38.901** or ray-tracing.

---

### Q10. What is EIRP and how does it relate to the link budget?
- **EIRP (Effective Isotropic Radiated Power):** The hypothetical power that an ideal isotropic antenna would need to radiate to produce the peak signal intensity observed in the main beam of the actual transmitter antenna:
  $$\text{EIRP}(\text{dBm}) = P_t(\text{dBm}) + G_t(\text{dBi}) - L_{\text{cable}}(\text{dB})$$
- In cellular networks, regulatory limits (FCC/TRAI) cap the maximum EIRP to prevent interference to neighboring cells.

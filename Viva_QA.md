# VIVA PREPARATION: QUESTIONS AND ANSWERS

### Course Details
- **Course:** 21CSE458T — Wireless and Mobile Communication
- **Project Title:** Comparative Analysis of Wireless Signal Propagation Models (Free Space, Okumura and Hata)
- **Team Members:**
  - Harsh Yadav (`RA2311003011546`)
  - Utkarsh Dabas (`RA2311003011550`)
  - Tamanna Singh (`RA2311003011570`)

---

### Q1: What is path loss, and why is it crucial in wireless communication system design?
**Answer:**  
Path loss ($PL$) is the attenuation or reduction in power density of an electromagnetic radio wave as it propagates from the transmitter to the receiver through the wireless channel. It is expressed logarithmically as:
$$PL(\text{dB}) = 10 \log_{10}\left(\frac{P_t}{P_r}\right)$$
It is fundamental to wireless engineering because it dictates the cell coverage radius, maximum allowable link budget, transmitter power requirements, handover boundaries, and base station density needed to maintain target Quality of Service (QoS).

---

### Q2: Why is the Free Space Path Loss (FSPL) model considered overly optimistic for terrestrial cellular networks?
**Answer:**  
FSPL assumes a completely unobstructed, sterile vacuum environment with 100% line-of-sight (LOS) clearance across all Fresnel zones, where power decays strictly following the inverse-square law ($n = 2$, or $20\text{ dB/decade}$).  
In real-world terrestrial cellular environments, electromagnetic waves encounter severe physical obstacles (buildings, terrain, foliage, atmospheric moisture) causing reflection, diffraction, scattering, and ground-bounce destructive interference. As a result, actual terrestrial path loss exponents range between $3.0$ and $5.0$, making FSPL severely underestimate signal loss (by up to $54.68\text{ dB}$ at $20\text{ km}$).

---

### Q3: What is the primary difference between the Okumura model and the Hata model?
**Answer:**  
- **Okumura Model (1968):** A purely empirical, graphical model derived from extensive drive-test field measurements in Tokyo, Japan. It presented path loss via graphical curves/nomograms and required manual interpolation, which made computer automation and programmatic network planning difficult.
- **Hata Model (1980):** Developed closed-form analytical mathematical equations that directly parameterized and fitted Okumura's graphical curves for urban, suburban, and rural environments within specified parameter ranges, enabling automated computerized radio frequency (RF) simulation.

---

### Q4: What are the valid operating parameter ranges for the Hata Model?
**Answer:**  
The Hata empirical formulations are strictly valid within the following empirical boundaries:
1. **Carrier Frequency ($f$):** $150\text{ MHz} \le f \le 1500\text{ MHz}$
2. **Base Station Effective Antenna Height ($h_{te}$):** $30\text{ m} \le h_{te} \le 200\text{ m}$
3. **Mobile Station Antenna Height ($h_{re}$):** $1\text{ m} \le h_{re} \le 10\text{ m}$
4. **Link Distance ($d$):** $1\text{ km} \le d \le 20\text{ km}$  
*Note:* Applying the Hata model outside these bounds (e.g., microcells with $d < 1\text{ km}$ or PCS/cellular bands $> 1500\text{ MHz}$) leads to severe inaccuracies; for frequencies up to $2000\text{ MHz}$, the COST-231 Hata extension must be used instead.

---

### Q5: How does carrier frequency affect path loss according to theoretical and empirical models?
**Answer:**  
In both theoretical and empirical models, higher carrier frequencies experience higher path loss:
- In **Free Space**, path loss scales as $20\log_{10}(f)$ because effective antenna aperture ($A_e = \frac{\lambda^2}{4\pi} = \frac{c^2}{4\pi f^2}$) decreases inversely with the square of frequency.
- In **Hata Urban**, path loss scales as $26.16\log_{10}(f)$, exhibiting an even steeper frequency penalty due to increased diffraction loss over rooftops and stronger material absorption at shorter wavelengths.

---

### Q6: What is the purpose of the mobile antenna height correction factor $a(h_{re})$ in the Hata model?
**Answer:**  
The correction factor $a(h_{re})$ accounts for local clutter, street geometry, and clutter clearance around the handheld receiver:
- For a small-to-medium city at $f = 900\text{ MHz}$ and $h_{re} = 1.5\text{ m}$:
  $$a(h_{re}) = (1.1\log_{10}(900) - 0.7)(1.5) - (1.56\log_{10}(900) - 0.8) \approx 0.00\text{ dB}$$
- If mobile height increases (e.g., mounted on a vehicle at $3\text{ m}$), $a(h_{re})$ increases, which is subtracted from path loss, representing improved line-of-sight and reduced street-level scattering.

---

### Q7: Based on your simulation results at $f = 900\text{ MHz}$, what are the exact path loss values at $1\text{ km}$ and $20\text{ km}$ across the three models?
**Answer:**  
From our numerical simulation:
- **At $1\text{ km}$:**
  - Free Space Path Loss: **$91.52\text{ dB}$**
  - Okumura (Open Area): **$97.90\text{ dB}$**
  - Hata (Urban Area): **$126.40\text{ dB}$**  
  *(Hata experiences $34.88\text{ dB}$ more loss than Free Space)*
- **At $20\text{ km}$:**
  - Free Space Path Loss: **$117.55\text{ dB}$**
  - Okumura (Open Area): **$143.73\text{ dB}$**
  - Hata (Urban Area): **$172.23\text{ dB}$**  
  *(The divergence expands to $54.68\text{ dB}$ penalty for Hata over Free Space, representing a factor of $>290,000$ in linear signal power attenuation).*

---

### Q8: Under what conditions should an RF engineer select the Okumura Open Area model instead of the Hata Urban model?
**Answer:**  
The Okumura Open Area model should be selected for rural deployments, farmland, highways, or open unpopulated plains where there are no dense multi-story concrete structures or continuous street corridors within $300-400\text{ m}$ of the transmission path.  
In our simulation, open area path loss is approximately **$28.5\text{ dB}$ lower** than urban path loss across all distances, reflecting the near-absence of man-made clutter and building shadowing.

---

### Q9: What are the main limitations of the Hata model for 4G LTE and 5G NR networks?
**Answer:**  
1. **Frequency Ceiling:** The classic Hata model is capped at $1.5\text{ GHz}$ (and COST-231 Hata at $2.0\text{ GHz}$), whereas 4G/5G operate across mid-bands ($3.5\text{ GHz}$) and mmWave bands ($28\text{ GHz}, 39\text{ GHz}$).
2. **Cell Size Constraint:** Hata requires $d \ge 1\text{ km}$ (macrocells), whereas modern 4G/5G deployments rely on dense microcells, picocells, and femtocells with radii of $50\text{ m}$ to $500\text{ m}$.
3. **Antenna Height Assumptions:** Hata assumes base stations are mounted well above average rooftop height ($h_{te} \ge 30\text{ m}$), whereas 5G small cells are mounted below rooftop level on street utility poles and building facades.  
*(Modern standards utilize 3GPP TR 38.901 models instead).*

---

### Q10: If the base station tower height is doubled from $30\text{ m}$ to $60\text{ m}$, how does the path loss change in the Hata model?
**Answer:**  
In Hata's formula, the base station height appears in two terms:
1. The constant term: $-13.82 \log_{10}(h_{te})$
2. The distance slope term: $-6.55 \log_{10}(h_{te}) \log_{10}(d)$

When $h_{te}$ doubles ($\log_{10}(2) \approx 0.30103$):
- Constant term reduction: $-13.82 \times 0.30103 \approx -4.16\text{ dB}$
- Slope term reduction at $d = 10\text{ km}$ ($\log_{10}(10) = 1$): $-6.55 \times 0.30103 \approx -1.97\text{ dB}$
- **Total Path Loss Reduction:** Approximately **$6.13\text{ dB}$**.  
Doubling the antenna tower height improves coverage and reduces path loss by over $6\text{ dB}$ (effectively quadrupling received signal power).


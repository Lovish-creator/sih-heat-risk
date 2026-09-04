# Wet Bulb Globe Temperature (WBGT) - Scientific Documentation

## 1. Scientific Concept & Occupational Domain
The **Wet Bulb Globe Temperature (WBGT)** (Yaglou & Minard, 1957; ISO 7243; NIOSH 2016) is the gold-standard environmental thermal index utilized globally for occupational safety, military operations, athletics, and heavy industrial labor.

While UTCI evaluates general ambient physiological strain across all body nodes, **WBGT is directly coupled to physical labor capacity, evaporative cooling potential, and radiant heat load on working personnel**.

---

## 2. Mathematical Equations

### Standard Outdoor WBGT Formulation (Direct Solar Load)
$$\text{WBGT}_{\text{outdoor}} = 0.7\,T_{\text{nw}} + 0.2\,T_{\text{g}} + 0.1\,T_{\text{a}}$$

### Indoor / In-Shade Formulation (No Solar Load)
$$\text{WBGT}_{\text{indoor}} = 0.7\,T_{\text{w}} + 0.3\,T_{\text{g}}$$

Where:
- $T_{\text{nw}}$: Natural wet-bulb temperature ($^\circ\text{C}$), reflecting cooling via ambient humidity and natural airflow.
- $T_{\text{w}}$: Psychrometric wet-bulb temperature ($^\circ\text{C}$).
- $T_{\text{g}}$: Black globe temperature ($^\circ\text{C}$), measuring radiative heat load from solar radiation and surface surroundings.
- $T_{\text{a}}$: Ambient dry-bulb air temperature ($^\circ\text{C}$).

---

## 3. Estimating WBGT from Standard Meteorological Measurements

### A. Psychrometric Wet-Bulb Temperature ($T_{\text{w}}$) - Stull (2011) Empirical Formula
For standard atmospheric pressure, Stull derived a highly accurate empirical expression valid for $-20^\circ\text{C} \le T_a \le 50^\circ\text{C}$ and $5\% \le \text{RH} \le 99\%$:

$$T_{\text{w}} = T_{\text{a}} \arctan\left(0.151977\,(\text{RH} + 8.313659)^{0.5}\right) + \arctan(T_{\text{a}} + \text{RH}) - \arctan(\text{RH} - 1.676331) + 0.00391838\,(\text{RH})^{1.5} \arctan(0.023101\,\text{RH}) - 4.686035$$

### B. Natural Wet-Bulb Temperature ($T_{\text{nw}}$)
In outdoor environments with natural wind $v$ ($\text{m/s}$):
$$T_{\text{nw}} \approx T_{\text{w}} + \delta_{\text{rad}}(S, v)$$
Where under moderate airflow ($v > 1.0\text{ m/s}$), $T_{\text{nw}}$ converges closely to psychrometric wet-bulb $T_{\text{w}}$.

### C. Black Globe Temperature ($T_{\text{g}}$) Estimation
Following the energy balance model of a standard 150mm matte-black copper sphere (Liljegren et al., 2008; Bernard & Pourmoghani):

$$T_{\text{g}} \approx T_{\text{a}} + \frac{0.0149 \times S}{v_{2\text{m}}^{0.6} + 0.05}$$

Where:
- $S$: Surface solar irradiance ($\text{W/m}^2$)
- $v_{2\text{m}}$: 2-meter wind speed ($\text{m/s}$) (scaled from 10m wind via $v_2 = v_{10} \times (2/10)^{0.2}$)
- $T_a$: Air temperature ($^\circ\text{C}$)

---

## 4. NIOSH Occupational Heat Exposure Thresholds & Regimens

| WBGT Range ($^\circ\text{C}$) | Risk Level | Prescribed NIOSH Work/Rest Regimen | Minimum Water Intake |
|:---|:---|:---|:---|
| **$< 28.0$** | **Low Risk** | Continuous strenuous work permissible ($45\text{--}60\text{ min/hr}$) | $0.5\text{ L / hour}$ |
| **$28.0 \text{ to } 30.0$** | **Moderate Risk** | $75\%$ Work / $25\%$ Rest each hour under shade | $0.75\text{ L / hour}$ |
| **$30.0 \text{ to } 32.0$** | **High Risk** | $50\%$ Work / $50\%$ Rest each hour under shade | $1.0\text{ L / hour}$ |
| **$> 32.0$** | **Extreme Danger** | $25\%$ Work / $75\%$ Rest or halt heavy outdoor labor | $1.0\text{ L / hour}$ + Electrolytes |

---

## 5. Limitations
1. Assumes standard light cotton work clothing (1.0 clo); impermeable chemical protective suits or heavy protective gear significantly increase heat accumulation.
2. Does not replace physical on-site WBGT sensors for OSHA/factory legal compliance.

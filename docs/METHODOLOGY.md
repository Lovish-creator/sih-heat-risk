# Scientific Methodology & Calculation Reference — Taapamigo (SIH26083)

**STATUS: SCIENTIFIC METHODOLOGY & FORMULATION REFERENCE**

---

## 1. End-to-End Methodological Pipeline

The Taapamigo platform executes an interpretable, physically grounded biometeorological risk pipeline:

```
[Meteorological Inputs: Ta, Tdp, RH, WS, Solar]
                       │
                       ▼
         [Biometeorological Modeling]
   ├── UTCI (COST 730 6th-order polynomial)
   ├── WBGT (Stull psychrometric + Liljegren solar)
   └── NOAA Heat Index (Rothfusz regression)
                       │
                       ▼
      [Composite Thermal Hazard Score (0–100)]
   Hazard = 0.45(UTCI_norm) + 0.35(WBGT_norm) + 0.20(HI_norm)
                       │
                       ▼
   [Census 2011 Demographic Vulnerability (0–100)]
   Vuln = 0.40(Elderly_norm) + 0.35(Labor_norm) + 0.25(Density_norm)
                       │
                       ▼
       [Heatwave Duration Persistence Factor]
   Duration multiplier based on consecutive days with Ta >= 40°C
                       │
                       ▼
     [Relative Heat-Health Risk Score (0–100)]
   Risk = 0.55(Hazard) + 0.30(Vulnerability) + 0.15(Duration)
                       │
                       ▼
         [IMD 4-Tier Alert Classification]
   Green (<25) | Yellow (25–49) | Orange (50–74) | Red (>=75)
                       │
                       ▼
   [GIS Ward Prioritization & Multi-Persona Advisories]
```

> **Calibration Disclaimer:**
> *"The weighting scheme is an interpretable prototype design and should be calibrated against local health outcome data before production use."*

---

## 2. Mathematical Formulations

### 2.1 Universal Thermal Climate Index (UTCI)

UTCI is defined as the equivalent ambient temperature ($^\circ\text{C}$) of a reference environment that produces the same physiological strain response (sweating, shivering, core temperature change) as the actual outdoor environment, based on the Fiala 187-node human thermoregulation model.

#### Water Vapor Pressure ($e$, hPa) — Magnus-Tetens Formulation
$$e = 6.112 \times \exp\left(\frac{17.67 \times T_a}{T_a + 243.5}\right) \times \left(\frac{RH}{100}\right)$$

#### Mean Radiant Temperature ($T_{mrt}$, $^\circ\text{C}$) — Stefan-Boltzmann Radiation Balance
$$T_{mrt} = \left[ (T_a + 273.15)^4 + \frac{f_p \cdot \alpha_k \cdot S}{\epsilon_p \cdot \sigma} \right]^{0.25} - 273.15$$
- $S$: All-sky shortwave solar irradiance ($W/m^2$)
- $f_p = 0.28$: Solar projection factor for standing human
- $\alpha_k = 0.70$: Solar absorption coefficient for skin/clothing
- $\epsilon_p = 0.97$: Human body emissivity
- $\sigma = 5.670374 \times 10^{-8}\text{ W}/(\text{m}^2\cdot\text{K}^4)$: Stefan-Boltzmann constant

#### 6th-Order Operational Polynomial
$$\Delta T_{mrt} = T_{mrt} - T_a$$
$$\text{UTCI} = T_a + \text{Offset}(T_a, \Delta T_{mrt}, v_{10m}, e)$$
Implemented via the 6th-order polynomial regression across 10 biometeorological stress categories:
- $> +46^\circ\text{C}$: Extreme Heat Stress (Hazard = 100)
- $+38^\circ\text{C} \text{ to } +46^\circ\text{C}$: Very Strong Heat Stress (Hazard = 80)
- $+32^\circ\text{C} \text{ to } +38^\circ\text{C}$: Strong Heat Stress (Hazard = 60)
- $+26^\circ\text{C} \text{ to } +32^\circ\text{C}$: Moderate Heat Stress (Hazard = 30)
- $+9^\circ\text{C} \text{ to } +26^\circ\text{C}$: No Thermal Stress (Hazard = 0)

---

### 2.2 Wet Bulb Globe Temperature (WBGT)

WBGT is the standard occupational heat stress metric (ISO 7243:2017 / NIOSH 2016).

#### Psychrometric Wet-Bulb Temperature ($T_w$, $^\circ\text{C}$) — Roland Stull (2011)
$$\begin{aligned}
T_w = T_a \cdot \arctan\left(0.151977 \sqrt{RH + 8.313659}\right) + \arctan(T_a + RH) - \arctan(RH - 1.676331) \\
+ 0.00391838 \cdot (RH)^{1.5} \cdot \arctan(0.023101 \cdot RH) - 4.686035
\end{aligned}$$

#### Black Globe Temperature ($T_g$, $^\circ\text{C}$) — Liljegren Solar Equilibrium
$$T_g = 0.01498 \cdot S + 1.184 \cdot T_a - 0.0789 \cdot RH - 0.723 \cdot v + 2.67$$

#### Outdoor & Indoor WBGT Equations
$$\text{WBGT}_{\text{outdoor}} = 0.7 \cdot T_w + 0.2 \cdot T_g + 0.1 \cdot T_a$$
$$\text{WBGT}_{\text{indoor/shade}} = 0.7 \cdot T_w + 0.3 \cdot T_a$$

---

### 2.3 NOAA/NWS Heat Index (Rothfusz Regression)

For $T_a \ge 27^\circ\text{C}$ and $RH \ge 40\%$, the full 9-parameter Rothfusz regression is computed:
$$\begin{aligned}
\text{HI} = -42.379 + 2.04901523 \cdot T_F + 10.14333127 \cdot RH - 0.22475541 \cdot T_F \cdot RH \\
- 0.00683783 \cdot T_F^2 - 0.05481717 \cdot RH^2 + 0.00122874 \cdot T_F^2 \cdot RH \\
+ 0.00085282 \cdot T_F \cdot RH^2 - 0.00000199 \cdot T_F^2 \cdot RH^2
\end{aligned}$$
Where $T_F = T_a \times \frac{9}{5} + 32$. Converted back to $^\circ\text{C}$ for output.

---

### 2.4 Composite Thermal Hazard Score (0–100)

$$\text{Hazard Score} = 0.45 \cdot H_{\text{UTCI}} + 0.35 \cdot H_{\text{WBGT}} + 0.20 \cdot H_{\text{HI}}$$
Where $H_{\text{UTCI}}, H_{\text{WBGT}}, H_{\text{HI}}$ are normalized piecewise hazard scores bounded in $[0, 100]$.

---

### 2.5 Demographic Vulnerability Score (0–100)

$$\text{Vulnerability Score} = 0.40 \cdot V_{\text{elderly}} + 0.35 \cdot V_{\text{labor}} + 0.25 \cdot V_{\text{density}}$$
- $V_{\text{elderly}} = \min(100, \frac{\text{Elderly } 60+\%}{15.0} \times 100)$
- $V_{\text{labor}} = \min(100, \frac{\text{Outdoor Worker } \%}{45.0} \times 100)$
- $V_{\text{density}} = \min(100, \frac{\text{Population Density per km}^2}{25000} \times 100)$

---

### 2.6 Heatwave Duration & Relative Risk Index

$$\text{Duration Multiplier} = 1.0 + \min(0.40, (\text{consecutive\_days} - 1) \times 0.10)$$
$$\text{Relative Heat-Health Risk} = \text{clamp}\Big(0.55 \cdot (\text{Hazard} \times \text{Duration}) + 0.30 \cdot \text{Vulnerability} + 0.15 \cdot (\text{Duration Factor} \times 100), 0, 100\Big)$$

---

## 3. Alert Level Classification

| Alert Level | Risk Score Range | Color Code | Action Directive |
|---|---|---|---|
| **GREEN (Normal)** | $0.0 \le \text{Risk} < 25.0$ | `#10b981` | Normal operations. Standard hydration awareness. |
| **YELLOW (Watch)** | $25.0 \le \text{Risk} < 50.0$ | `#f59e0b` | Heat watch. Advise elderly and outdoor workers to take shaded breaks. |
| **ORANGE (Alert)** | $50.0 \le \text{Risk} < 75.0$ | `#f97316` | Severe heat alert. Mandatory 25% rest cycle for outdoor labor; prepare water distribution. |
| **RED (Warning)** | $75.0 \le \text{Risk} \le 100.0$ | `#ef4444` | Extreme heat emergency. Halt heavy outdoor labor during 12:00–16:00; activate cooling shelters and hospital emergency protocols. |

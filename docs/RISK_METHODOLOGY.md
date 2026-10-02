# Risk Methodology & Scientific Formulation — Taapamigo (SIH26083)

This document provides the complete mathematical and biometeorological specification for thermal hazard quantification, demographic vulnerability weighting, heatwave persistence modeling, and relative heat-health risk classification in Taapamigo.

---

## 1. The Tri-Factor Risk Conceptual Framework

Taapamigo operationalizes the disaster risk framework established by the **Intergovernmental Panel on Climate Change (IPCC SREX / AR6)**:

$$\text{Risk} = f(\text{Hazard}, \text{Vulnerability}, \text{Exposure / Persistence})$$

```mermaid
graph TD
    subgraph Hazard_Component [1. Thermal Hazard Engine]
        UTCI[UTCI Physiological Strain: 60%]
        WBGT[WBGT Occupational Strain: 25%]
        HI[NOAA Heat Index: 15%]
        THS[Composite Thermal Hazard Score: H in 0-100]
    end

    subgraph Vulnerability_Component [2. Demographic Vulnerability Engine]
        ELD[Elderly Pop 60+ Weight: 40%]
        LAB[Informal Outdoor Laborers: 35%]
        DEN[Population Density: 25%]
        UHI[LCZ Microclimate Heat Offset]
        DVI[Demographic Vulnerability Score: V in 0-100]
    end

    subgraph Persistence_Component [3. Heat Duration Engine]
        DUR[Consecutive Heatwave Days: N_days]
        PERS[Duration Score: D_score in 0-100 (Step Function)]
    end

    UTCI & WBGT & HI --> THS
    ELD & LAB & DEN & UHI --> DVI
    DUR --> PERS

    THS & DVI & PERS --> FINAL_RISK["Composite Relative Risk: R = 0.55*H + 0.30*V + 0.15*D (0-100)"]
```

---

## 2. Physiological Thermal Hazard Indices

### 2.1 Universal Thermal Climate Index (UTCI)
The Universal Thermal Climate Index is based on the **Fiala 6th-order multi-node human thermoregulation model** (COST Action 730 / Bröde et al., 2012). It calculates the equivalent ambient temperature of a reference environment producing the same dynamic physiological response (sweating, shivering, skin blood flow, rectal core temperature):

$$\text{UTCI} = T_a + \Delta \text{UTCI}(T_a, v_{10m}, e_a, T_{mrt} - T_a)$$

Where:
* $T_a$ = Dry-bulb air temperature ($^\circ\text{C}$, valid range: $-50^\circ\text{C} \le T_a \le +50^\circ\text{C}$)
* $v_{10m}$ = Wind speed at 10m height ($m/s$, operational polynomial validity range: $0.5 \le v_{10m} \le 17.0\text{ m/s}$)
* $e_a$ = Water vapor pressure ($\text{hPa}$, derived from relative humidity $\text{RH}$ via Magnus-Tetens equation, clamped to $50.0\text{ hPa}$)
* $T_{mrt}$ = Mean radiant temperature ($^\circ\text{C}$)

#### Water Vapor Pressure ($e_a$):
$$e_s(T_a) = 6.112 \cdot \exp\left(\frac{17.67 \cdot T_a}{T_a + 243.5}\right)$$
$$e_a = e_s(T_a) \cdot \frac{\text{RH}}{100}$$

#### UTCI Stress Categories:
| UTCI Range ($^\circ\text{C}$) | Thermal Stress Category | Physiological Meaning |
|:---|:---|:---|
| $> +46$ | **Extreme Heat Stress** | Severe risk of heat stroke, core temperature rapid rise |
| $+38 \text{ to } +46$ | **Very Strong Heat Stress** | High cardiovascular strain, rapid dehydration |
| $+32 \text{ to } +38$ | **Strong Heat Stress** | Moderate thermoregulatory strain, sweat rate $> 0.5\text{ L/h}$ |
| $+26 \text{ to } +32$ | **Moderate Heat Stress** | Minor discomfort for sensitive populations |
| $+9 \text{ to } +26$ | **No Thermal Stress** | Thermal neutrality |

---

### 2.2 Wet Bulb Globe Temperature (WBGT)
WBGT models occupational and athletic heat strain in outdoor environments under direct solar radiation (ISO 7243:2017 & Liljegren et al., 2008):

$$\text{WBGT}_{\text{outdoor}} = 0.7 \cdot T_{nw} + 0.2 \cdot T_g + 0.1 \cdot T_a$$

Where:
* $T_{nw}$ = Natural wet-bulb temperature ($^\circ\text{C}$, radiative-convective-evaporative heat balance of a wet wick)
* $T_g$ = Black globe temperature ($^\circ\text{C}$, radiative-convective heat balance of a 150mm matte black sphere)
* $T_a$ = Ambient dry-bulb temperature ($^\circ\text{C}$)

#### ISO / NIOSH Work-Rest Action Thresholds:
| WBGT Range ($^\circ\text{C}$) | Flag Color | NIOSH Regimen (Moderate Work) | Hydration Requirement |
|:---|:---|:---|:---|
| $< 27.8$ | **White** | Continuous normal work | $0.5\text{ L/h}$ water |
| $27.8 \text{ to } 29.4$ | **Green** | 45 min work / 15 min rest per hour | $0.75\text{ L/h}$ water + electrolytes |
| $29.4 \text{ to } 31.1$ | **Yellow** | 30 min work / 30 min rest per hour | $1.0\text{ L/h}$ ORS / electrolytes |
| $31.1 \text{ to } 32.2$ | **Red** | 15 min work / 45 min rest per hour | $1.0\text{ L/h}$ strict monitoring |
| $\ge 32.2$ | **Black** | **Cease all strenuous outdoor labor** | Immediate cooling access |

---

### 2.3 NOAA Heat Index (Apparent Temperature)
The Rothfusz 9-term polynomial equation (Steadman, 1979; NOAA NWS):

$$\text{HI} = c_1 + c_2 T + c_3 R + c_4 T R + c_5 T^2 + c_6 R^2 + c_7 T^2 R + c_8 T R^2 + c_9 T^2 R^2$$

With standard coefficients ($c_1 = -42.379, c_2 = 2.04901523, \dots$) evaluated for $T \ge 80^\circ\text{F}$ ($26.7^\circ\text{C}$) and $\text{RH} \ge 40\%$.

---

### 2.4 Composite Thermal Hazard Score ($H$)
The individual indices are normalized to $[0, 100]$ scales and combined via a calibrated weighted average:

$$H = w_{\text{utci}} \cdot S(\text{UTCI}) + w_{\text{wbgt}} \cdot S(\text{WBGT}) + w_{\text{hi}} \cdot S(\text{HI})$$

Canonical scientific weights (authoritative in `docs/MODEL_SPEC.md`):
$$w_{\text{utci}} = 0.60, \quad w_{\text{wbgt}} = 0.25, \quad w_{\text{hi}} = 0.15 \quad (\Sigma w = 1.0)$$

---

## 3. Demographic Vulnerability Index ($V$)

Census 2011 Primary Census Abstract (PCA) indicators are normalized per municipal ward:

$$V = 100 \cdot \left( w_{\text{eld}} \cdot \tilde{P}_{\text{elderly}} + w_{\text{lab}} \cdot \tilde{P}_{\text{laborers}} + w_{\text{den}} \cdot \tilde{D}_{\text{pop}} \right) + \Delta V_{\text{LCZ}}$$

Where:
* $\tilde{P}_{\text{elderly}} = \frac{\text{Elderly } 60+ \text{ Pct}}{30.0\%}$ (capped at 1.0, weighted at $0.40$)
* $\tilde{P}_{\text{laborers}} = \frac{\text{Outdoor Workers Pct}}{50.0\%}$ (capped at 1.0, weighted at $0.35$)
* $\tilde{D}_{\text{pop}} = \frac{\text{Density}}{25,000 \text{ persons/km}^2}$ (capped at 1.0, weighted at $0.25$)
* $\Delta V_{\text{LCZ}} \in [0, 10]$ = Microclimate heat retention penalty based on Local Climate Zone classification (e.g. LCZ 1 Compact High-Rise: $+8$, LCZ 2 Compact Mid-Rise: $+6$, LCZ 9 Sparsely Built: $+1$).

---

## 4. Heatwave Duration Score ($D_{\text{score}}$)

Consecutive days of extreme heat compound human physiological strain and nocturnal heat retention. The engine evaluates consecutive days where $T_{\max} \ge 40.0^\circ\text{C}$ or departure from normal $\ge +4.5^\circ\text{C}$ using a discrete duration scaling function $f_D$:

$$D_{\text{score}} = f_D(\text{consecutive\_days}) \times 100.0$$

* **Day 1:** $f_D = 0.00 \implies D_{\text{score}} = 0.0$
* **Day 2:** $f_D = 0.33 \implies D_{\text{score}} = 33.0$
* **Day 3:** $f_D = 0.66 \implies D_{\text{score}} = 66.0$
* **Day 4+:** $f_D = 1.00 \implies D_{\text{score}} = 100.0$

---

## 5. Composite Relative Heat-Health Risk Score ($R$)

The unified ward relative risk score is calculated as an additive multi-criteria linear combination:

$$R = \text{clamp}\Big( w_H \cdot H + w_V \cdot V + w_D \cdot D_{\text{score}}, \; 0.0, \; 100.0 \Big)$$

Canonical baseline weights (authoritative in `docs/MODEL_SPEC.md`):
$$w_H = 0.55, \quad w_V = 0.30, \quad w_D = 0.15 \quad (\Sigma w = 1.0)$$

### 5.1 Day-1 Theoretical Maximum Quirk
Because $D_{\text{score}} = 0.0$ on Day 1, the maximum achievable risk score on Day 1 is:
$$\text{Max Risk}_{\text{Day 1}} = 0.55(100.0) + 0.30(100.0) + 0.15(0.0) = 85.0$$
This mathematical guardrail prevents declaring maximum emergency alert status on a single isolated hot afternoon without cumulative persistence.

### 5.2 Risk Tier Classification
| Risk Score ($R$) | Risk Category | Color Code | Action Required |
|:---|:---|:---|:---|
| $0.0 \le R < 25.0$ | **GREEN (Normal)** | 🟢 Green (`#10b981`) | Normal routine, standard hydration awareness |
| $25.0 \le R < 50.0$ | **YELLOW (Watch)** | 🟡 Yellow (`#f59e0b`) | Advisory issued for elderly, shaded rest for outdoor workers |
| $50.0 \le R < 75.0$ | **ORANGE (Alert)** | 🟠 Orange (`#f97316`) | Municipal cooling shelters opened, strict work-rest schedules |
| $75.0 \le R \le 100.0$ | **RED (Warning)** | 🔴 Red (`#ef4444`) | High-priority emergency alerts, suspension of outdoor manual labor |

### 5.3 Presentation Reconciliation
- **Presentation Slide 3:** Accurately displays the additive formulation ($0.55\text{ Hazard} + 0.30\text{ Vulnerability} + 0.15\text{ Duration}$).
- **Presentation Slide 4:** Contains the conceptual shorthand $\text{Risk} = \text{Hazard} \times \text{Vulnerability} \times \text{Duration}$, representing the UNDRR paradigm that risk arises from the interaction of all three elements. In software calculation, the additive model above is implemented to prevent mathematical collapse when duration is 0 on Day 1.

---

## 6. Scientific Limitations & Disclaimers

> **IMPORTANT SCIENTIFIC DISCLAIMER:**  
> The Composite Heat-Health Risk Index ($R$) is a **relative spatial prioritization metric** intended for early warning and municipal resource dispatch. It does **not** represent a clinical prediction of individual medical morbidity or absolute statistical mortality. For clinical protocols, refer to the **NCDC National Action Plan for Heat-Related Illnesses (2024)**.

# Authoritative Model Specification — Taapamigo (SIH 2026 PS26083)

**Model Version:** `1.0.0-prototype`  
**Classification:** Multi-Criteria Linear Relative Heat-Health Risk Model (Deterministic Tier-1)  
**Standard Status:** Single Authoritative Source of Truth for Equations, Weights, and Thresholds

---

## 1. Executive Summary & Purpose

This document establishes the single authoritative specification for the Taapamigo Relative Heat-Health Risk Index engine. All application modules (`backend/app/risk/engine.py`, `backend/app/thermal/hazard.py`, `backend/app/vulnerability/demographic.py`), configuration files (`config/risk_weights.yaml`), documentation, and automated tests are programmatically verified against the parameters defined herein.

### 1.1 Operational Role & Scope
- **Intended Purpose:** Spatial prioritization and relative risk differentiation across municipal wards and urban centers to inform resource dispatch (water distribution, shaded shelters, cooling centers, labor suspension advisories).
- **Non-Clinical Disclaimer:** This model computes a **relative vulnerability-exposure priority score** on a $[0, 100]$ scale. It is **not** an epidemiological casualty forecast, clinical diagnostic tool, or empirical statistical mortality prediction (e.g., Distributed Lag Non-linear Model / DLNM).
- **Calibration Status:** The weights ($0.55 / 0.30 / 0.15$ and subcomponent weights) represent an **expert-judgment prototype design** grounded in international biometeorological guidelines (WMO/WHO 2015, ISO 7243:2017, NIOSH 2016, COST Action 730). They have not yet been fitted to municipal all-cause excess mortality registries.

---

## 2. Master Formulation: Composite Relative Heat-Health Risk

The composite risk score $R \in [0, 100]$ is computed as an **additive multi-criteria linear combination** of three normalized dimensions:

$$R = \text{clamp}\Big( w_H \cdot H + w_V \cdot V + w_D \cdot D_{\text{score}}, \; 0.0, \; 100.0 \Big)$$

### 2.1 Top-Level Component Weights
The component weights are strictly constrained to sum to $1.0$:

| Dimension | Symbol | Weight ($w$) | Theoretical Rationale |
| :--- | :---: | :---: | :--- |
| **Thermal Hazard** | $H$ | **`0.55`** | Primary environmental driver; directly induces physiological and cardiovascular strain. |
| **Demographic Vulnerability** | $V$ | **`0.30`** | Population susceptibility modifier (elderly physiology, outdoor exertion, urban density). |
| **Heatwave Duration** | $D_{\text{score}}$ | **`0.15`** | Cumulative physiological depletion and nocturnal non-recovery penalty. |

$$\Sigma w = w_H + w_V + w_D = 0.55 + 0.30 + 0.15 = 1.00$$

---

## 3. Subcomponent Specifications

### 3.1 Thermal Hazard Score ($H \in [0, 100]$)
Derived from three peer-reviewed human biometeorological and apparent temperature indices:

$$H = w_{\text{utci}} \cdot S(\text{UTCI}) + w_{\text{wbgt}} \cdot S(\text{WBGT}) + w_{\text{hi}} \cdot S(\text{HI})$$

| Metric | Symbol | Weight | Standard / Foundation | Normalization $S(\cdot)$ |
| :--- | :---: | :---: | :--- | :--- |
| **Universal Thermal Climate Index** | $\text{UTCI}$ | **`0.60`** | COST Action 730 / Fiala 6th-order multi-node model | Piecewise linear mapping from $[-50, +60]^\circ\text{C}$ equivalent temp |
| **Wet Bulb Globe Temperature** | $\text{WBGT}$ | **`0.25`** | ISO 7243:2017 / NIOSH 2016 occupational standard | Piecewise linear mapping from $[20, 36]^\circ\text{C}$ work-rest scale |
| **NOAA Heat Index** | $\text{HI}$ | **`0.15`** | Rothfusz (1990) / Steadman (1979) shade apparent temp | Normalized apparent temperature $[25, 55]^\circ\text{C}$ |

$$\Sigma w_{\text{hazard}} = 0.60 + 0.25 + 0.15 = 1.00$$

### 3.2 Demographic Vulnerability Score ($V \in [0, 100]$)
Synthesized from Census of India 2011 baseline indicators normalized by empirical metropolitan thresholds:

$$V = 100.0 \cdot \Big( w_{\text{eld}} \cdot \tilde{P}_{\text{elderly}} + w_{\text{work}} \cdot \tilde{P}_{\text{workers}} + w_{\text{den}} \cdot \tilde{D}_{\text{pop}} \Big)$$

| Indicator | Symbol | Weight | Normalization Formula |
| :--- | :---: | :---: | :--- |
| **Elderly Population Share (Age $\ge 60$)** | $\tilde{P}_{\text{elderly}}$ | **`0.40`** | $\min(1.0, \frac{\text{Elderly Share}}{0.30})$ (capped at 30% baseline) |
| **Outdoor Worker Share** | $\tilde{P}_{\text{workers}}$ | **`0.35`** | $\min(1.0, \frac{\text{Worker Share}}{0.50})$ (capped at 50% baseline) |
| **Population Density** | $\tilde{D}_{\text{pop}}$ | **`0.25`** | $\min(1.0, \frac{\text{Density}}{25,000 \text{ persons/km}^2})$ (capped at 25,000) |

$$\Sigma w_{\text{vuln}} = 0.40 + 0.35 + 0.25 = 1.00$$

> **Data Provenance Reality:** Primary Census Abstract (PCA) tables do not contain age $60+$ figures (published in C-Series C-13/C-14), and pool informal construction/gig workers into "Other Workers". Derived counts are transparently flagged as `"data_quality": "estimated"`.

### 3.3 Heatwave Duration Score ($D_{\text{score}} \in [0, 100]$)
Evaluates consecutive days where maximum air temperature $T_{\max} \ge 40.0^\circ\text{C}$ or departure from normal $\ge +4.5^\circ\text{C}$:

$$D_{\text{score}} = f_D(\text{consecutive\_days}) \times 100.0$$

The discrete duration scaling function $f_D$:

| Consecutive Heatwave Days | Duration Multiplier ($f_D$) | Duration Score ($D_{\text{score}}$) | Physiological Context |
| :---: | :---: | :---: | :--- |
| **Day 1** | **`0.00`** | **`0.0`** | Acute onset; physiological heat reserves intact. |
| **Day 2** | **`0.33`** | **`33.0`** | Emerging nocturnal sleep disruption and baseline strain. |
| **Day 3** | **`0.66`** | **`66.0`** | Severe thermoregulatory fatigue, cumulative electrolyte loss. |
| **Day 4+** | **`1.00`** | **`100.0`** | Critical cardiovascular depletion, maximum persistent penalty. |

---

## 4. Mathematical Quirk & Guardrail: Day-1 Maximum Risk

A notable property of this model formulation arises directly from the duration step function:

$$\text{On Day 1: } D_{\text{score}} = 0.0$$

Consequently, under maximum environmental hazard ($H = 100.0$) and maximum demographic vulnerability ($V = 100.0$):

$$\text{Max Risk}_{\text{Day 1}} = 0.55 \times 100.0 + 0.30 \times 100.0 + 0.15 \times 0.0 = 85.0$$

- **Theoretical Implication:** A single isolated spike day cannot reach a risk score of $100.0$.
- **Operational Justification:** Disaster management authorities do not declare top-tier sustained emergency status without multi-day heatwave persistence, guarding against premature over-escalation on single atypical hot afternoons.

---

## 5. Alert Level Classification Bands

Continuous risk scores $R \in [0, 100]$ map to the standard 4-tier alert system harmonized with India Meteorological Department (IMD) conventions:

| Alert Tier | Score Range | Color Code | Hex Code | Municipal Action Directive |
| :--- | :---: | :---: | :---: | :--- |
| **GREEN (Normal)** | $[0.0, 25.0)$ | 🟢 Green | `#10b981` | Normal municipal operations; routine public hydration awareness. |
| **YELLOW (Watch)** | $[25.0, 50.0)$ | 🟡 Yellow | `#f59e0b` | Heat watch; targeted advisories for senior citizens and outdoor laborers. |
| **ORANGE (Alert)** | $[50.0, 75.0)$ | 🟠 Orange | `#f97316` | Severe heat alert; activate water distribution and mandatory 25% rest cycles. |
| **RED (Warning)** | $[75.0, 100.0]$ | 🔴 Red | `#ef4444` | Extreme heat emergency; cease heavy outdoor labor 12:00–16:00; activate cooling shelters. |

---

## 6. Reconciliation with Presentation Shorthand

- **Presentation Slide 3:** Explicitly presents the additive formulation $0.55\text{ Hazard} + 0.30\text{ Vulnerability} + 0.15\text{ Duration}$. This matches the software engine.
- **Presentation Slide 4:** Contains the shorthand expression $\text{Risk} = \text{Hazard} \times \text{Vulnerability} \times \text{Duration}$. This is the standard UNDRR conceptual paradigm illustrating that risk emerges from the intersection of all three elements. In software execution, the additive model above is implemented to prevent mathematical collapse when duration is 0 on Day 1.

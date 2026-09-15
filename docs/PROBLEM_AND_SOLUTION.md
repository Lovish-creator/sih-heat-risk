# Problem & Solution — Taapamigo (SIH26083)

**STATUS: TIER 1 IMPLEMENTATION OVERVIEW**

---

## 1. The Problem: The Heat Crisis in India

Extreme heatwaves pose a severe, escalating threat to public health, urban infrastructure, and economic productivity across India. However, existing early warning and response workflows face critical limitations:

1. **Reliance on Air Temperature Alone ($T_a$):**
   Standard weather forecasts report dry-bulb air temperature, which fails to represent human thermal physiological strain. A dry $42^\circ\text{C}$ in Rajasthan may impose less cardiovascular and thermoregulatory strain than a humid $37^\circ\text{C}$ with $75\%$ relative humidity in coastal Chennai or Mumbai, where evaporative cooling through sweating is completely suppressed.

2. **Neglect of Solar Radiation & Wind Speed:**
   Outdoor laborers and vulnerable citizens under direct solar irradiance experience massive radiant heat loads (Mean Radiant Temperature, $T_{mrt}$), which air temperature measurements inside Stevenson screens do not capture.

3. **Homogeneous City-Wide Warnings:**
   Conventional heatwave warnings are issued at coarse district or city scales (e.g., "Heatwave in Delhi"). However, heat risk varies drastically across municipal wards due to differences in population density, elderly demographics, informal housing, and outdoor occupational exposure.

4. **Lack of Actionable, Persona-Specific Guidance:**
   Generic advice ("stay indoors") is impractical for daily wage outdoor workers, street vendors, and municipal field staff. Municipal authorities need ward-specific prioritization to deploy emergency water tankers, adjust work shifts, and alert healthcare centers.

---

## 2. Our Solution: Taapamigo

**Taapamigo** is an early warning and human thermal stress decision-support system built to bridge the gap between atmospheric science and municipal public health action.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             THE 6-STAGE WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [1. Weather Ingestion]                                                     │
│     ├── Real-time Open-Meteo public API (Ta, Tdp, RH, Wind, Pressure)       │
│     └── NASA POWER surface solar irradiance (All-sky shortwave W/m²)        │
│                            │                                                │
│                            ▼                                                │
│  [2. Thermal Stress Calculation]                                            │
│     ├── Universal Thermal Climate Index (UTCI COST 730 polynomial)          │
│     ├── Wet Bulb Globe Temperature (WBGT ISO 7243 / Stull psychrometric)    │
│     ├── NOAA/NWS Rothfusz Heat Index                                        │
│     └── Normalized Composite Thermal Hazard Score (0–100)                   │
│                            │                                                │
│                            ▼                                                │
│  [3. Population Vulnerability Estimation]                                   │
│     ├── Census of India 2011 Primary Census Abstract (PCA) demographics     │
│     ├── Elderly Population Proportion (Age 60+)                             │
│     ├── Outdoor Agricultural & Marginal Worker Proportion                   │
│     └── Population Density per km²                                          │
│                            │                                                │
│                            ▼                                                │
│  [4. Heat Persistence & Relative Risk Synthesis]                            │
│     ├── Multi-day consecutive heatwave duration factor (1.0x – 1.4x)        │
│     └── Relative Heat-Health Risk Score (0–100) mapped to IMD 4-tier alerts │
│                            │                                                │
│                            ▼                                                │
│  [5. GIS Ward Prioritization]                                               │
│     ├── Interactive Leaflet choropleth map across 26 municipal corporations │
│     └── Decision-support side drawer ("Why is this ward high risk?")        │
│                            │                                                │
│                            ▼                                                │
│  [6. Actionable Advisory Generation]                                        │
│     ├── 4 Persona Categories (Citizens, Workers, Municipal, Health)         │
│     ├── Mandatory NIOSH labor/rest cycle recommendations                    │
│     └── ITU/WMO CAP v1.2 emergency alert XML/JSON & SMS broadcast payloads  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. What Makes the Workflow Effective

- **Biometeorological Grounding:** Evaluates *what weather does to the human body* by calculating international physiological metrics (UTCI, WBGT, Heat Index) from multi-parameter inputs ($T_a, RH, WS, Solar$).
- **Demographic Vulnerability Integration:** Combines physical heat hazard with Census 2011 PCA population vulnerability indicators to identify where high hazard coincides with exposed, vulnerable human populations.
- **Micro-Spatial Decision Support:** Allows municipal commissioners and disaster management cells to immediately see which specific wards require emergency intervention.
- **Transparent & Defensible:** Uses peer-reviewed mathematical regressions and publicly verifiable data sources with zero synthetic claims or ungrounded mortality predictions.

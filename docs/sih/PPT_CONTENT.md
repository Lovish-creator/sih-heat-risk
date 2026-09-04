# SIH26083 - 6-Slide Presentation Content & Pitch Deck Guide

This document formats the project's technical architecture, scientific foundation, and operational feasibility into the standard **6-Slide Smart India Hackathon (SIH) presentation format**.

---

## SLIDE 1 — TITLE & PROJECT OVERVIEW
- **Problem Statement ID**: SIH26083
- **Title**: Extreme Heatwave Early Warning and Human Thermal Stress Index
- **Organization**: Ministry of Earth Sciences (MoES) / National Centre for Medium Range Weather Forecasting (NCMRWF)
- **Category / Theme**: Software / Disaster Management
- **Project Name**: **ThermoShield India** (Human Biometeorological Thermal Risk & Early Warning Platform)
- **Core Philosophy**: *"Moving from what the weather IS to what the weather DOES to human beings."*

---

## SLIDE 2 — THE PROBLEM: WHY AIR TEMPERATURE IS INSUFFICIENT
- **The Core Flaw in Conventional Warnings**:
  - Current alerts rely solely on dry-bulb temperature ($T_a \ge 40^\circ\text{C}$ or $+4.5^\circ\text{C}$ anomaly).
  - **The Biometeorological Reality**: A dry, windy $40^\circ\text{C}$ day allows evaporative sweat cooling ($\text{UTCI} \approx 35^\circ\text{C}$), whereas a humid, stagnant, high-solar $40^\circ\text{C}$ day prevents sweat evaporation, causing lethal physiological heat strain ($\text{UTCI} > 48^\circ\text{C}$, Extreme Heat Stress).
- **The Demographic Disparity**:
  - Blanket city-wide alerts treat all neighborhoods identically.
  - Wards with high concentrations of outdoor laborers (construction, gig workers, agriculture) and elderly citizens ($60+$) face disproportionately severe heat stroke risks.
- **Evidence-Based Health Burden**:
  - NCDC 2024 NPCCHH surveillance reports thousands of heat stroke cases during Indian pre-monsoon heatwaves.
  - Azhar et al. (2014) documented $+43\%$ excess mortality during the May 2010 Ahmedabad heatwave.

---

## SLIDE 3 — TECHNICAL APPROACH & SCIENTIFIC ARCHITECTURE
- **Multi-Parameter Physics Pipeline**:
  - Integrates 2m Air Temp ($T_a$), Relative Humidity ($\text{RH}$), 10m Wind Speed ($v_{10}$), and Solar Irradiance ($S$).
- **Dual Physiological Engines**:
  1. **Universal Thermal Climate Index (UTCI)**: 6th-order polynomial (240+ terms) modeling whole-body human energy balance and mean radiant temperature ($T_{mrt}$).
  2. **NIOSH Wet Bulb Globe Temperature (WBGT)**: Stull psychrometric natural wet-bulb + Liljegren black-globe radiation model for occupational labor capacity.
- **Vulnerability & GIS Attribution**:
  - Ingests Census 2011 Primary Census Abstract (elderly $60+$ share, outdoor worker share, population density).
  - Performs **Ward-Level Risk Attribution** via Leaflet GIS choropleth without making false claims of micro-scale meteorological resolution.
- **Actionable Advisory Engine**:
  - Automated, persona-tailored guidance for Citizens, Outdoor Workers (NIOSH rest schedules), and Municipal Authorities (NCDC Heat Action Plan protocols).

---

## SLIDE 4 — FEASIBILITY, VIABILITY & REPRODUCIBILITY
- **100% Tier-1 Automated Open Data MVP**:
  - NASA POWER API (automated meteorological & solar radiation ingestion).
  - Census 2011 (open demographic baseline).
  - IMD open warning definitions & NCDC / WHO clinical guidelines.
- **Zero Proprietary API Locks**:
  - Runs out of the box with zero paid API keys, zero human approval barriers.
  - Deterministic `DEMO_MODE=true` ensures 100% reliability during live hackathon judging.
- **Modular Enterprise Backend**:
  - FastAPI asynchronous backend with 14 documented REST endpoints.
  - Containerized deployment via Docker and Docker Compose.
- **Future-Ready Integration Adapters**:
  - Built-in `NCMRWFProvider` and `MOSDACProvider` stubs ready for institutional GRIB2 / INSAT satellite feeds in Phase-2.

---

## SLIDE 5 — IMPACT, TARGET BENEFICIARIES & VALUE CREATION
- **Target Beneficiaries**:
  1. **Informal Outdoor Workers & Laborers**: Receive hourly WBGT-based work-rest cycles and hydration benchmarks, reducing occupational heat stroke.
  2. **Vulnerable Citizens & Elderly ($60+$)**: Early 3–5 day anticipation to avoid peak outdoor thermal exposure (11:00–16:00).
  3. **Municipal Corporations (Disaster Management)**: Spatial prioritization of emergency cooling shelters, drinking water tankers, and hospital heatstroke bed preparation.
- **Honest & Defensible Impact**:
  - Replaces arbitrary black-box AI with transparent, scientifically proven biometeorological physics.
  - Provides an interpretable **Relative Heat-Health Risk Index (0–100)** rather than fabricating ungrounded clinical death counts.

---

## SLIDE 6 — AUTHORITATIVE RESEARCH & REFERENCES
1. **Bröde, P. et al. (2012)**: *Deriving the operational procedure for the Universal Thermal Climate Index (UTCI)*. Int. J. Biometeorol., 56(3), 481-494.
2. **NIOSH / CDC (2016)**: *Criteria for a Recommended Standard: Occupational Exposure to Heat and Hot Environments*. DHHS (NIOSH) Pub. No. 2016-106.
3. **National Centre for Disease Control (NCDC, 2024)**: *National Action Plan for Heat-Related Illnesses (NAP-HRI)*, MoHFW, Govt. of India.
4. **India Meteorological Department (IMD)**: *Heat Wave Guidance & Impact-Based Forecasting Guidelines*.
5. **Azhar, G. S. et al. (2014)**: *Heat-Related Mortality in India: Excess All-Cause Mortality Associated with the 2010 Ahmedabad Heat Wave*. PLOS ONE, 9(3), e91831.
6. **World Health Organization (WHO, 2021)**: *Heat and Health Factsheet & Guidelines for Heat-Health Action Plans*.

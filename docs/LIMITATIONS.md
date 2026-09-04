# Honest Technical & Scientific Limitations

This document provides a transparent accounting of the scientific boundaries, data constraints, and assumptions embedded within the SIH26083 Tier-1 prototype.

---

## 1. Spatial Resolution vs Meteorological Grid

### The Physical Reality
- **NASA POWER Meteorological Data**: Provided at a nominal spatial resolution of $0.5^\circ \times 0.625^\circ$ ($\approx 50\text{ km} \times 60\text{ km}$), with solar radiation at $1.0^\circ \times 1.0^\circ$.
- **Municipal Wards**: Typically span $1\text{ to } 10\text{ km}^2$.

### Our Honest Distinction
- **What We Do**: We perform **Ward-Level Risk Attribution**. We take the regional environmental forcing field (temperature, humidity, wind, solar radiation) and join it with localized, ward-specific demographic vulnerability (elderly ratio, outdoor worker ratio, population density).
- **What We Do NOT Claim**: We **never** claim that NASA POWER or regional reanalysis models provide micro-scale ward-resolution meteorological forecasts. Microclimatic variations (e.g., street canyon wind channeling, localized asphalt heat traps) require micro-scale Computational Fluid Dynamics (CFD) or dense hyper-local IoT weather station meshes.

---

## 2. Demographic Baseline: Census 2011

### The Data Constraint
- The latest published decennial Census in India with ward-level Primary Census Abstract (PCA) indicators is the **Census of India 2011**.

### Mitigation & Prototype Handling
- In the prototype, Census 2011 data serves as a **normalized relative vulnerability baseline**.
- The pipeline computes normalized demographic sensitivity indices ($0\text{--}100$) based on relative distributions across wards rather than raw population projections.
- In production, when the upcoming Census or updated municipal voter/electoral registries become available, the demographic ingestion adapter seamlessly ingests the updated tables without altering the underlying risk engine.

---

## 3. Mortality & Health Impact: Relative Risk vs Absolute Death Counts

### The Scientific Boundary
- Predicting absolute mortality counts ("$N$ people will die tomorrow") without validated daily ward-level all-cause mortality registries, clinical hospital admission records, and fitted Distributed Lag Non-linear Models (DLNM) is scientifically indefensible and ungrounded.

### Our Solution
- Health impact is quantified as an interpretable **Relative Heat-Health Risk Score (0–100)** and categorized into IMD-aligned action levels (Green, Yellow, Orange, Red).
- The metric indicates elevated physiological vulnerability and population sensitivity, providing municipal authorities with an operational decision-support tool.

---

## 4. Operational Numerical Weather Prediction (NWP)

### Scope in Tier-1 Prototype
- NASA POWER analysis-ready data is used for automated ingestion and daily meteorological trend analysis.
- An explicit **NCMRWF Integration Adapter** (`backend/app/data_sources/ncmrwf_stub.py`) is architected with complete schemas, defining the exact transformation required to ingest NCMRWF NCUM GRIB2/NetCDF binary forecast fields once institutional credentials (Tier-2) are configured.

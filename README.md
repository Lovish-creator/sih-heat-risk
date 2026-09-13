# ThermoShield India

## SIH26083 — Extreme Heatwave Early Warning and Human Thermal Stress Index

---

## Current Status

```
CURRENT STATUS:
TIER 1 — WORKING PROTOTYPE
```

> **"A functional proof-of-concept demonstrating the complete heat-risk decision-support workflow using available public data, transparent scientific calculations, demographic vulnerability indicators, GIS prioritization, and rule-based advisories."**

*The hosted demonstration is already deployed. Local execution instructions are provided below for reproducibility and development.*

---

## 1. Problem

Extreme heatwaves pose a severe and escalating public health challenge across India. However, existing early warning and response workflows face major limitations:

1. **Air Temperature Alone is Insufficient:** Standard weather forecasts report dry-bulb air temperature ($T_a$), which ignores humidity, wind, and solar radiation. A humid $38^\circ\text{C}$ in Chennai or Mumbai causes far greater cardiovascular and thermoregulatory strain than a dry $42^\circ\text{C}$ in Rajasthan because evaporative cooling (sweating) is suppressed.
2. **Homogeneous City-Wide Warnings:** Conventional warnings treat entire cities as uniform blocks. In reality, heat risk varies significantly across municipal wards due to differences in building density, informal housing, elderly populations, and outdoor worker concentrations.
3. **Lack of Actionable, Persona-Specific Guidance:** General advice ("stay indoors") is impractical for daily wage outdoor laborers, street vendors, and municipal field staff. Municipal authorities need ward-level prioritization to deploy emergency water tankers, adjust working hours, and alert local health centers.

---

## 2. Our Solution

**ThermoShield India** is an early warning and human thermal stress decision-support system that translates meteorological forecasts into localized public health actions.

The system evaluates *what weather does to human physiology* by calculating international biometeorological stress indices (UTCI, WBGT, Heat Index), combining them with Census demographic vulnerability indicators, and visualizing ward-level prioritization on an interactive GIS map.

---

## 3. What Is Implemented Now (Tier-1 Prototype)

The current repository contains a fully functional Tier-1 prototype with these confirmed capabilities:

- **Public Weather Ingestion:** Ingests live surface temperature, humidity, wind, and pressure from Open-Meteo public endpoints and solar radiation ($W/m^2$) from NASA POWER.
- **Biometeorological Physics Core:**
  - **Universal Thermal Climate Index (UTCI):** Official COST 730 6th-order polynomial approximation.
  - **Wet Bulb Globe Temperature (WBGT):** Stull (2011) psychrometric wet-bulb + Liljegren black globe radiative equilibrium for outdoor and shade environments per ISO 7243 / NIOSH 2016.
  - **NOAA/NWS Heat Index:** 9-parameter Rothfusz regression with Steadman low-range boundary.
  - **Composite Thermal Hazard:** Normalized hazard score on a continuous $0–100$ scale.
- **Census 2011 Demographic Vulnerability:** Pre-compiled baseline tables covering 46 Indian districts (Elderly 60+, Outdoor labor fraction, Population density).
- **Relative Heat-Health Risk Engine:** Interpretable continuous score ($0–100$) combining thermal hazard, demographic vulnerability, and multi-day heat persistence, mapped to IMD 4-tier alert levels (Green, Yellow, Orange, Red).
- **GIS Municipal Ward Mapping:** Interactive Leaflet choropleth map with bundled vector boundaries for 26 Indian municipal corporations (Delhi 290 wards, Bengaluru 243 wards, Chennai 155 wards, Kolkata 141 wards, Hyderabad 145 wards, Lucknow 112 wards, Abohar 50 wards, etc.) and Stewart-Oke (2012) Local Climate Zone spatial units for other locations.
- **Decision-Support Side Drawer:** Explains *why* a specific ward is at elevated risk (thermal load vs. demographic vulnerability) and suggests targeted municipal actions.
- **5-Day Forecast Analytics:** Interactive charts for 5-day risk trajectories, biometeorological metric comparison, weather drivers, and 24-hour diurnal heat tables.
- **Actionable Advisories:** Tailored guidance for 4 distinct personas (Citizens, Outdoor Workers, Municipal Authorities, Health/Emergency Departments) aligned with NCDC NAP-HRI 2024 and NDMA guidelines.
- **CAP v1.2 Emergency Alerts:** Generates ITU/WMO Common Alerting Protocol XML/JSON payloads and citizen SMS broadcast text.
- **FastAPI Backend & REST API:** 18 operational endpoints for weather, thermal stress, risk scoring, GIS boundaries, geocoding, and advisories.
- **Automated Test Suite:** 51 passing unit and integration tests with deterministic offline mocks.

---

## 4. How It Works

The platform processes data through a transparent, 6-stage pipeline:

```
[1. Weather Data Ingestion]
   ├── Open-Meteo Public API (Ta, Tdp, RH, Wind, Pressure)
   └── NASA POWER (Surface Solar Radiation W/m²)
          │
          ▼
[2. Thermal Stress Calculation]
   ├── UTCI (COST 730 6th-order polynomial)
   ├── WBGT (ISO 7243 / NIOSH / Stull psychrometric)
   ├── NOAA Heat Index (Rothfusz regression)
   └── Composite Thermal Hazard Score (0–100)
          │
          ▼
[3. Population Vulnerability Estimation]
   ├── Census of India 2011 Primary Census Abstract (PCA)
   ├── Elderly Population Proportion (Age 60+)
   ├── Outdoor Labor & Marginal Worker Proportion
   └── Population Density per km²
          │
          ▼
[4. Relative Risk Score Synthesis]
   ├── Multi-day heatwave duration factor (Ta >= 40°C persistence)
   └── Relative Risk = (0.55 × Hazard) + (0.30 × Vulnerability) + (0.15 × Duration)
          │
          ▼
[5. GIS Ward Prioritization]
   ├── Interactive Leaflet choropleth map across 26 cities
   └── Decision-support side drawer ("Why is this location high risk?")
          │
          ▼
[6. Actionable Advisories]
   ├── 4 Target Personas (Citizens, Workers, Municipal, Health)
   └── ITU/WMO CAP v1.2 emergency alert payloads & citizen SMS
```

---

## 5. What Is Not Yet Implemented (Explicit Boundaries)

To maintain complete scientific and technical honesty, the Tier-1 prototype explicitly does **NOT** include:

- **Mortality Prediction:** The system does not predict death counts, mortality rates, or mortality probabilities.
- **Hospitalization Prediction:** The system does not forecast emergency room admissions or hospital bed demand.
- **Patient-Level Health Data:** No private electronic health records, patient data, or live hospital surveillance feeds are connected.
- **Live Institutional NCMRWF Integration:** Direct high-throughput binary GRIB/NetCDF feeds from NCMRWF supercomputers require formal institutional credentials (modeled as a Tier-2 connector interface).
- **Live Institutional IMD Integration:** IMD data is referenced for climatological normal departures and heatwave thresholds; live internal push APIs are not connected.
- **Validated Machine-Learning Models:** The `ml/` package provides architecture scaffolding; no ML model is trained without verified health outcome labels.
- **Automated Government Alert Dispatch:** The platform generates CAP v1.2 payloads and preview text; live automated telecom gateway dispatch requires institutional agreements.

---

## 6. Tier 2 Roadmap (Data-Connected Pilot)

**STATUS: FUTURE DEVELOPMENT**

> *"Tier 2 would convert the prototype into a data-connected pilot through verified datasets, operational ingestion, historical validation, and controlled institutional integration."*

Key Tier-2 goals:
1. Ingest official municipal ward delimitation vector files verified by State Election Commissions.
2. Deploy PostgreSQL/PostGIS operational database with spatial indexing.
3. Establish scheduled ingestion pipelines (Celery/Airflow) for NWP model cycles (00, 06, 12, 18 UTC).
4. Connect live IMD and NCMRWF institutional data feeds under data access agreements.
5. Ingest aggregated, de-identified heat-related illness records from pilot municipal hospitals.
6. Calibrate risk weights using empirical Distributed Lag Non-linear Models (DLNM).
7. Retrospectively backtest the system against major historical Indian heatwave events.
8. Conduct controlled field pilots with 1–2 target Municipal Corporations.

---

## 7. Tier 3 Vision (Production-Scale System)

**STATUS: FUTURE VISION**

> *"Tier 3 is the long-term production vision requiring institutional partnerships, validated health data, operational infrastructure, scientific calibration, governance, and government deployment approvals."*

Key Tier-3 goals:
1. Nationwide operational coverage across all 28 states, 8 Union Territories, and 4,000+ urban local bodies.
2. Direct coupling to NCMRWF NCUM 4km regional models and IMD Automatic Weather Station grids.
3. Satellite Land Surface Temperature (LST) coupling from ISRO INSAT-3D and Sentinel-3.
4. Micro-scale urban canopy and heat-island modeling at 100m–500m resolution.
5. Integration with MoHFW Integrated Health Information Platform (IHIP) syndromic surveillance.
6. Integration with National Disaster Management Authority (NDMA) SACHET emergency broadcast system.
7. Deployment on MeghRaj (Government of India Cloud) / NIC high-availability infrastructure.
8. Compliance with Digital Personal Data Protection Act (DPDPA 2023) and statutory nodal approvals.

---

## 8. Data Sources Summary

| Source | Actual Use | Access Type | Current Status | Limitation |
|---|---|---|---|---|
| **Open-Meteo API** | Live surface weather ($T_a, T_{dp}, RH, WS, P, UV$) & 5-day forecasts | Public REST API | **Connected and used** | Point/grid forecasts from global models; not a dedicated physical station in every ward. |
| **NASA POWER API** | Surface solar downward irradiance ($W/m^2$) | Public REST API | **Connected and used** | Satellite-derived reanalysis and radiation balance. |
| **Census of India 2011 PCA** | Baseline demographic indicators (Elderly, Workers, Density) | Static Local Dataset | **Static local dataset** | Historical 2011 baseline data. |
| **DataMeet / Delimitation** | Vector ward polygons for 26 municipal corporations | Static Local GeoJSON | **Static local dataset** | Open civic datasets and state gazette delimitation boundaries. |
| **OpenStreetMap / Nominatim** | Base map tiles and reverse geocoding | Public Web Service | **Connected and used** | Cached locally (24h TTL) to adhere to OSM policies. |
| **UTCI / WBGT / Heat Index** | Biometeorological formulas | Pure Python Algorithms | **Connected and used** | Deterministic peer-reviewed mathematical regressions. |
| **IMD / NCDC Guidance** | Climatological departures and advisory protocols | Reference Standards | **Reference only** | Used for algorithmic thresholds; internal push APIs are not connected. |
| **NCMRWF Unified Model** | Target NWP model core | Architecture Stub | **Future integration** | Requires institutional access; modeled as Tier-2 connector. |

---

## 9. Limitations

1. **Relative Prioritization:** The Relative Heat-Health Risk Score ($0–100$) is an environmental and demographic exposure estimate to guide resource allocation. It is not a clinical diagnosis or mortality prediction.
2. **Sensor Density:** Meteorological data is derived from open public APIs and downscaled via Local Climate Zones ($A_w = \text{Pop}_w / \text{Density}_w$); every ward does not have an independent physical weather sensor.
3. **Census Baseline:** Demographic vulnerability uses Census 2011 PCA tables; contemporary population shifts over the past decade are not dynamically captured.
4. **Institutional Coupling:** Direct feeds from NCMRWF supercomputers, IMD internal systems, and hospital databases require Tier-2/3 institutional agreements.

---

## 10. Local Setup & Execution

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- `pip` (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lovish-creator/sih-heat-risk.git
   cd sih-heat-risk
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database tables (optional local seed):**
   ```bash
   python scripts/seed_db.py
   ```

5. **Start the local server:**
   ```bash
   python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

6. **Open in browser:**
   Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 11. API Documentation

When the local server is running:
- **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Technical Reference:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Comprehensive Markdown API Reference:** [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md)

---

## 12. Demonstration Flow for Evaluators

1. **Overview Dashboard:** View the **Relative Heat-Health Risk Score** ($0–100$), IMD alert badge, and biometeorological metrics (UTCI, WBGT, Heat Index, Air Temp).
2. **Jurisdiction Selection:** Switch between 26 pre-packaged municipal corporations (Delhi 290 wards, Bengaluru 243 wards, Chennai 155 wards, Abohar 50 wards, Ahmedabad 20 wards, etc.).
3. **GIS Risk Map:** Click the **🗺️ GIS Risk Map** tab. Click any ward polygon on the map to open the **Decision-Support Side Drawer** ("Why is this unit high risk?").
4. **GPS & Global Coordinates:** Click **📍 Detect Location** to analyze current GPS coordinates or enter manual latitude/longitude.
5. **5-Day Forecast Analytics:** Click **📈 5-Day Forecast** to inspect 5-day risk trajectories, biometeorological metric comparison, and the 24-hour diurnal heat cycle table.
6. **Demographic Vulnerability:** Click **👥 Demographic Vulnerability** to inspect Census 2011 PCA indicators and export risk data to CSV.
7. **Actionable Advisories:** Click **🚨 Actionable Advisories** to view protocols for Citizens, Outdoor Workers (NIOSH work-rest cycles), Municipal Authorities, and Health Departments.
8. **CAP v1.2 Emergency Alerts:** Click **🚨 CAP Alert** in the header to view standardized Common Alerting Protocol XML/JSON and citizen SMS broadcast text.
9. **Data Provenance Audit:** Click **📖 Data & Provenance Audit** to review the transparent data matrix and interactive formula calculator.

---

## 13. Documentation Index

| Document | Purpose |
|---|---|
| [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) | Authoritative Tier-1 scope and explicit exclusions |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | Tier 2 Pilot, Tier 3 Production vision, comparison table, and transition plan |
| [`docs/PROBLEM_AND_SOLUTION.md`](docs/PROBLEM_AND_SOLUTION.md) | The SIH problem statement and 6-stage solution workflow |
| [`docs/FEATURES.md`](docs/FEATURES.md) | Confirmed demonstrable Tier-1 features |
| [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) | Authoritative data source registry and classification |
| [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) | Complete scientific equations and biometeorological physics reference |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Tier-1 architecture and future Tier-2/3 distributed architecture |
| [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) | Complete REST API endpoint reference |
| [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) | Transparent technical and scientific boundaries |
| [`docs/DEMO_GUIDE.md`](docs/DEMO_GUIDE.md) | Step-by-step evaluator demonstration flow |
| [`docs/HEALTH_DATA_READINESS.md`](docs/HEALTH_DATA_READINESS.md) | Statutory health data constraints and epidemiological readiness |
| [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md) | Model card for deterministic baseline and future ML extension |
| [`ml/README.md`](ml/README.md) | Machine learning policy and future research scaffolding |

---

## 14. Automated Tests

Run the complete test suite:
```bash
python -m pytest -v
```

**Test Status:** 51 / 51 tests passing (100% pass rate with deterministic offline mocks).

---

## License

This project is released under the **MIT License** — see [`LICENSE`](LICENSE) for details.

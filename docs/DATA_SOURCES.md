# Data Sources & Provenance Registry — Taapamigo (SIH 2026 PS26083)

**Document Version:** 2.0.0 (Consolidated)  
**Standard Status:** Single Authoritative Data Provenance & Access Tier Matrix  
**Reconciliation Notice:** Incorporates and supersedes `docs/TIER_STATUS.md`.

---

## 1. Single Authoritative Source Registry Table

| Source Name | Organization / Origin | Actual Use in Platform | Access Type | Operational Status | Scientific & Technical Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Open-Meteo Weather API** | Open-Meteo GmbH / Open Data | Near-real-time surface observations ($T_a, T_{dp}, RH, WS, P, UV$) and 5-day forecasts | Public REST API (No Key Required) | **Tier 1 (Automated)** | Point/grid forecasts derived from global NWP models (DWD ICON, GFS, ECMWF); not dedicated ward-level physical AWS sensors. |
| **NASA POWER API** | NASA Langley Research Center | All-sky shortwave solar downward irradiance ($W/m^2$) and direct normal irradiance | Public REST API (No Key Required) | **Tier 1 (Automated)** | Satellite-derived reanalysis and assimilation; latency of recent days bridged via solar geometry algorithms. |
| **Census of India 2011 PCA** | Office of the Registrar General & Census Commissioner, India | Baseline demographic indicators (Elderly 60+, Outdoor workers, Population density) | Static Local Dataset (`data/sample/`) | **Tier 1 (Static Open)** | Census 2011 is historical baseline. Crucially, PCA lacks Age 60+ data (published in C-13/C-14) and pools construction workers into "Other Workers". Derived counts are tagged `"data_quality": "estimated"`. |
| **Municipal Ward Boundaries (DataMeet & Delimitation)** | DataMeet Community / Municipal Gazette Notifications | Vector polygons for ward-level GIS choropleth mapping across 26 cities | Static Local GeoJSON (`data/datameet_wards/`, `data/sample/`) | **Tier 1 (Static Open)** | Civic community boundaries and gazetted delimitations. Statutory towns without released ward GIS shapefiles utilize Stewart & Oke (2012) LCZ spatial units. |
| **OpenStreetMap & Nominatim** | OpenStreetMap Foundation | Base map tiles and reverse/forward geocoding of coordinates | Public Open Web Service | **Tier 1 (Automated)** | Subject to OSM usage policies; cached locally (24h TTL) to prevent rate limiting. |
| **UTCI Biometeorological Model** | COST Action 730 / ISB Commission 6 | Operational polynomial calculation of Universal Thermal Climate Index | Deterministic Python Algorithm (`backend/app/thermal/utci.py`) | **Tier 1 (Physics Engine)** | 6th-order operational polynomial strictly validated within $-50.0^\circ\text{C} \le T_a \le +50.0^\circ\text{C}$ and $0.5\text{ m/s} \le v_{10m} \le 17.0\text{ m/s}$ (Bröde et al., 2012). |
| **WBGT Occupational Model** | ISO 7243:2017 / NIOSH 2016 / Stull (2011) | Psychrometric wet-bulb and Liljegren radiative black globe temperature calculation | Deterministic Python Algorithm (`backend/app/thermal/wbgt.py`) | **Tier 1 (Physics Engine)** | Stull empirical formulation valid for $-20^\circ\text{C} \le T_a \le +50^\circ\text{C}$ and $5\% \le RH \le 99\%$. |
| **NOAA/NWS Heat Index** | NOAA / National Weather Service (Rothfusz, 1990) | Apparent temperature regression under high temperature and humidity | Deterministic Python Algorithm (`backend/app/thermal/heat_index.py`) | **Tier 1 (Physics Engine)** | 9-parameter regression calibrated for $T_a \ge 27^\circ\text{C}$ and $RH \ge 40\%$; Steadman linear equation used below these bounds. |
| **IMD Heatwave Guidance & Thresholds** | India Meteorological Department (MoES) | Climatological departure criteria ($+4.5^\circ\text{C}$ to $+6.4^\circ\text{C}$) and 4-tier alert level definitions | Reference Guidelines (`backend/app/data_sources/imd_adapter.py`) | **Tier 1 (Guidelines)** | Used for algorithmic threshold definitions; live institutional IMD internal push feeds are not connected in Tier 1. |
| **NCDC National Action Plan (NAP-HRI 2024)** | National Centre for Disease Control (MoHFW) | Advisory directives, medical readiness protocols, and vulnerable group guidance | Reference Guidelines (`backend/app/advisory/engine.py`) | **Tier 1 (Guidelines)** | Encapsulates official medical guidelines into rule-based advisory templates. |
| **NCMRWF Unified Model NWP** | National Centre for Medium Range Weather Forecasting (MoES) | Target numerical weather prediction model core (NCUM 4km / 12km) | Architecture Connector Interface (`backend/app/data_sources/ncmrwf_stub.py`) | **Tier 2 (Connector Stub)** | Requires formal institutional authorization and binary GRIB/NetCDF ingestion pipeline; modeled as a Tier-2 connector interface. |
| **ISRO MOSDAC Satellite Products** | ISRO Space Applications Centre | INSAT-3D/3DR Land Surface Temperature (LST) | Architecture Interface | **Tier 2 (Account Required)** | Requires individual developer registration and HMAC SHA-256 tokens on MOSDAC portal. |
| **IHIP / Hospital Heat Illness Telemetry** | MoHFW / State Health Departments | Daily hospital admissions and syndromic heatstroke registries | Target Architecture (`docs/HEALTH_DATA_READINESS.md`) | **Tier 3 (Restricted)** | Protected health information (PHI) under statutory privacy frameworks; no hospital records are ingested or fabricated in Tier 1. |

---

## 2. Institutional Access Tier Classification Matrix

| Tier | Operational Definition | Status in Current Prototype | Production Requirements |
| :--- | :--- | :--- | :--- |
| **Tier 1** | Publicly accessible without credentials, institutional approval, or private agreements. | **100% Automated & Reproducible** via public REST APIs, static open datasets, and open physics engines. | None; fully autonomous and reproducible out-of-the-box. |
| **Tier 2** | Public/Government services requiring individual account registration, API tokens, or binary file ingestion (GRIB2/NetCDF). | **Connector Interfaces & Stub Models Implemented** (e.g. `ncmrwf_stub.py`). | Formal registration on MoES NCMRWF / ISRO MOSDAC portals; configure `.env` tokens. |
| **Tier 3** | Restricted institutional datasets, patient health telemetry, municipal confidential records. | **Interface Schemas Defined; Non-Clinical Relative Risk Scoring** (zero synthetic health data). | Formal MoU with MoHFW/NCDC, Institutional Review Board (IRB) ethics clearance, State IDSP data-sharing agreements. |

---

## 3. Data Truthfulness & Provenance Commitments

1. **Zero Synthetic Mortality / Morbidity Claims:** The platform does not fabricate hospital admissions, heat stroke casualties, or death counts.
2. **Transparent Demographic Quality Labels:** Census PCA limitations are explicitly disclosed; all derived district/ward demographics carry `"data_quality": "estimated"` or `"is_illustrative": true`.
3. **No Claim of Unverified Ward-Level Weather Sensors:** Atmospheric forcing is obtained via public weather APIs and spatially attributed across municipal wards, modulated by demographic vulnerability and Local Climate Zone (LCZ) microclimate parameters.

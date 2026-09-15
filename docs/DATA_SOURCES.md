# Data Sources & Provenance Registry — Taapamigo (SIH26083)

**STATUS: ACCURATE DATA SOURCE REGISTRY**

---

## 1. Single Authoritative Source Registry Table

| Source Name | Organization / Origin | Actual Use in Platform | Access Type | Current Status | Scientific & Technical Limitations |
|---|---|---|---|---|---|
| **Open-Meteo Weather API** | Open-Meteo GmbH / Open Data | Near-real-time surface observations ($T_a, T_{dp}, RH, WS, P, UV$) and 5-day forecasts | Public REST API (No Key Required) | **A. Connected and used** | Point/grid forecasts derived from global numerical models (e.g. DWD ICON, GFS); not a dedicated ward-level physical ground station. |
| **NASA POWER API** | NASA Langley Research Center | All-sky shortwave solar downward irradiance ($W/m^2$) and direct normal irradiance | Public REST API (No Key Required) | **A. Connected and used** | Satellite-derived reanalysis and assimilation; latency of recent days bridged via real-time solar estimation formulations. |
| **Census of India 2011 PCA** | Office of the Registrar General & Census Commissioner, India | Baseline demographic indicators (Elderly 60+, Outdoor workers, Population density) | Static Local Dataset (`data/sample/`) | **B. Static local dataset** | Census 2011 is historical baseline data; dynamic contemporary population shifts are unmodeled in Tier 1. |
| **Municipal Ward Boundaries (DataMeet & Delimitation)** | DataMeet Community / Municipal Gazette Notifications | Vector polygons for ward-level GIS choropleth mapping across 26 cities | Static Local GeoJSON (`data/datameet_wards/`, `data/sample/`) | **B. Static local dataset** | Open geospatial boundaries compiled from open civic data initiatives and state delimitation notifications; not all ULBs in India have released digital GIS boundaries. |
| **OpenStreetMap & Nominatim** | OpenStreetMap Foundation | Base map tiles and reverse/forward geocoding of coordinates | Public Open Web Service | **A. Connected and used** | Subject to OSM usage policies; cached locally (24h TTL) to prevent rate limiting. |
| **UTCI Biometeorological Model** | COST Action 730 / ISB Commission 6 | Operational polynomial calculation of Universal Thermal Climate Index | Deterministic Python Algorithm (`backend/app/thermal/utci.py`) | **A. Connected and used** | 6th-order polynomial approximation valid within $-50^\circ\text{C} \le T_a \le +60^\circ\text{C}$ and $v_{10m} \le 30.3\text{ m/s}$. |
| **WBGT Occupational Model** | ISO 7243:2017 / NIOSH 2016 / Stull (2011) | Psychrometric wet-bulb and Liljegren radiative black globe temperature calculation | Deterministic Python Algorithm (`backend/app/thermal/wbgt.py`) | **A. Connected and used** | Stull empirical formula valid for $-20^\circ\text{C} \le T_a \le +50^\circ\text{C}$ and $5\% \le RH \le 99\%$. |
| **NOAA/NWS Heat Index** | NOAA / National Weather Service (Rothfusz, 1990) | Apparent temperature regression under high temperature and humidity | Deterministic Python Algorithm (`backend/app/thermal/heat_index.py`) | **A. Connected and used** | 9-parameter regression calibrated for $T_a \ge 27^\circ\text{C}$ and $RH \ge 40\%$; Steadman linear equation used below these bounds. |
| **IMD Heatwave Guidance & Thresholds** | India Meteorological Department (MoES) | Climatological departure criteria ($+4.5^\circ\text{C}$ to $+6.4^\circ\text{C}$) and 4-tier alert level definitions | Reference Guidelines (`backend/app/data_sources/imd_adapter.py`) | **C. Reference only** | Used for algorithmic threshold definitions; live institutional IMD internal push feeds are not connected in Tier 1. |
| **NCDC National Action Plan (NAP-HRI 2024)** | National Centre for Disease Control (MoHFW) | Advisory directives, medical readiness protocols, and vulnerable group guidance | Reference Guidelines (`backend/app/advisory/engine.py`) | **C. Reference only** | Encapsulates official medical guidelines into rule-based advisory templates. |
| **NCMRWF Unified Model NWP** | National Centre for Medium Range Weather Forecasting (MoES) | Target numerical weather prediction model core (NCUM 4km / 12km) | Architecture Connector Interface (`backend/app/data_sources/ncmrwf_stub.py`) | **D. Future integration** | Requires formal institutional authorization and binary GRIB/NetCDF ingestion pipeline; modeled as a Tier-2 connector interface. |
| **IHIP / Hospital Heat Illness Telemetry** | MoHFW / State Health Departments | Daily hospital admissions and syndromic heatstroke registries | Target Architecture (`docs/HEALTH_DATA_READINESS.md`) | **E. Not implemented** | Protected health data under statutory privacy frameworks; no hospital records are ingested or fabricated in Tier 1. |

---

## 2. Classification Key

- **A. Connected and used:** Actively queried over the network or executed programmatically in the running Tier-1 application.
- **B. Static local dataset:** Pre-compiled, verified local data files bundled with the application repository.
- **C. Reference only:** Scientific literature, standards, or government guidelines used to define algorithmic logic and thresholds.
- **D. Future integration:** Interface contracts, adapter stubs, or schemas prepared for future institutional access.
- **E. Not implemented:** Excluded from the current prototype; reserved for future authorized production stages.

---

## 3. Data Truthfulness Commitment

1. **Zero Synthetic Mortality / Hospitalization Claims:** The platform does not fabricate hospital admissions, heat stroke casualties, or death counts.
2. **Transparent Fallback Identification:** When specific ward demographic values are unavailable, the system explicitly flags the use of a baseline proxy.
3. **No Claim of Unverified Sensors:** The system transparently documents that meteorological forcing is obtained via public weather APIs and Local Climate Zone spatial parameters, not independent physical weather stations in every ward.

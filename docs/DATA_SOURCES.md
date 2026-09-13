# Data Sources & Provenance Register — ThermoShield India (SIH26083)

This document provides a transparent, verifiable register of all external data streams, APIs, demographic records, boundary datasets, and biometeorological standards integrated into ThermoShield India.

---

## 1. Master Data Sources Matrix

| Source Name | Provider / Authority | Official Portal URL | Ingestion Method | Cadence | License / Access | Variables Ingested |
|:---|:---|:---|:---|:---|:---|:---|
| **Open-Meteo Weather API** | Open-Meteo GmbH | [https://open-meteo.com/](https://open-meteo.com/) | REST API (JSON) | 15-min live / Hourly 7-day | Open Database License (ODbL) / CC-BY 4.0 | $T_a$, $\text{RH}$, $T_d$, Wind Speed (10m), Direct/Diffuse Solar Flux, Surface Pressure, Rain |
| **NASA POWER** | NASA Langley Research Center | [https://power.larc.nasa.gov/](https://power.larc.nasa.gov/) | REST API (JSON) | Daily / Climatological | Public Domain (US Gov) | All-sky Surface Shortwave Downward Irradiance (`ALLSKY_SFC_SW_DWN`), Top-of-Atmosphere Insolation |
| **IMD Climatology & Normals** | India Meteorological Department (MoES) | [https://mausam.imd.gov.in/](https://mausam.imd.gov.in/) | Official Gazettes & Climatological Tables | Climatological reference (1981-2010 / 1991-2020) | Open Government Data (OGD India) | Baseline station maximum temperatures, climatological heatwave departure criteria ($+4.5^\circ\text{C}, +6.4^\circ\text{C}$) |
| **NCMRWF Unified Model** | NCMRWF (MoES) | [https://www.ncmrwf.gov.in/](https://www.ncmrwf.gov.in/) | Numerical Model Architecture Reference | Deterministic 4km regional | Open Scientific Documentation | Spatial downscaling parameterization and high-resolution atmospheric boundary layer modeling |
| **Census of India 2011** | Office of the Registrar General & Census Commissioner, India | [https://censusindia.gov.in/](https://censusindia.gov.in/) | Primary Census Abstract (PCA) Tables | Decennial baseline | Open Government Data (OGD India) | Ward-level total population, elderly ($60+$), children ($0-5$), main/marginal outdoor laborers, household density |
| **OpenStreetMap & Overpass** | OpenStreetMap Foundation | [https://www.openstreetmap.org/](https://www.openstreetmap.org/) | Overpass API & PBF Extracts | Static GIS boundary dataset | ODbL (Open Database License) | Municipal boundary polygons, road density, open space extents |
| **Nominatim Geocoding** | OpenStreetMap Foundation | [https://nominatim.openstreetmap.org/](https://nominatim.openstreetmap.org/) | REST API (JSON) | On-demand geocoding | ODbL (Open Database License) | Lat/Lon to administrative hierarchy reverse resolution |
| **Esri World Imagery** | Environmental Systems Research Institute (Esri) | [https://www.esri.com/](https://www.esri.com/) | TMS Tile Service | On-demand UI tiles | Free developer tier / Web Tile terms | High-resolution satellite basemap imagery for spatial verification |
| **Municipal Corporation Gazettes** | State Urban Development Departments | [https://lgpunjab.gov.in/](https://lgpunjab.gov.in/) (and respective state portals) | Delimitation Notification Gazettes | Official statutory delimitation | Public Domain / Official State Gazettes | Official ward numbers and ward name lists (e.g. Abohar 50 wards, Ahmedabad 48 wards) |

---

## 2. Physiological & Biometeorological Standards

| Standard / Index | Governing Body / Authors | Primary Scientific Reference | Formula Type | Validation Dataset |
|:---|:---|:---|:---|:---|
| **Universal Thermal Climate Index (UTCI)** | International Society of Biometeorology (ISB) / COST Action 730 | Bröde et al. (2012) *Int J Biometeorol* 56(3):481-494 | 6th-order multi-node heat balance regression (Fiala model) | Validated against 240,000 human multi-node thermal comfort trials |
| **Wet Bulb Globe Temperature (WBGT)** | International Organization for Standardization (ISO) / NIOSH | ISO 7243:2017 & Liljegren et al. (2008) *J Occup Environ Hyg* 5(5):332-341 | Radiative-convective equilibrium heat balance | NIOSH Occupational Criteria for Work in Hot Environments (Pub 2016-106) |
| **NOAA Heat Index** | National Oceanic and Atmospheric Administration (NOAA) / NWS | Rothfusz, L. P. (1990) *NWS Technical Attachment SR 90-23* & Steadman (1979) | Multi-variable polynomial approximation | Human skin evaporative cooling and clothing resistance model |
| **Local Climate Zones (LCZ)** | American Meteorological Society (AMS) | Stewart, I. D. & Oke, T. R. (2012) *Bull. Amer. Meteor. Soc.* 93(12):1879-1900 | Biophysical urban surface classification | 17 standard LCZ classes for urban heat island modeling |
| **National Action Plan for Heat-Related Illnesses (NAP-HRI)** | National Centre for Disease Control (NCDC), MoHFW | NCDC NAP-HRI 2024 Guidelines | Public health thresholds & clinical intervention matrices | Ministry of Health & Family Welfare heatwave response framework |

---

## 3. Provenance Transparency & Fallback Protocols

To ensure uncompromising academic and scientific integrity:

1. **Explicit Geometry Provenance:**
   - Every ward record in the database includes `is_official_geometry`, `is_generated_geometry`, and `geometry_source`.
   - Where surveyed sub-meter surveyor shapefiles are not openly distributed by the municipality, boundaries are calculated via density-proportional Voronoi/geometric delimitations ($A_w = \text{Pop}_w / \text{Density}_w$) and explicitly marked as `is_generated_geometry: true`.
2. **Explicit Observation Fallback Logging:**
   - Every ingested atmospheric observation is tagged with `is_fallback: boolean` and `fallback_reason: string | null`.
   - In `APP_ENV=production` mode with `ENABLE_FALLBACK_DATA=false`, missing telemetry raises strict 503 Service Unavailable errors rather than silently substituting synthetic data.
3. **No Fabricated Clinical Data:**
   - ThermoShield does not fabricate hospital admissions or mortality counts.
   - A dedicated Health Data Readiness specification ([`HEALTH_DATA_READINESS.md`](HEALTH_DATA_READINESS.md)) defines the exact protocol for integrating genuine State IDSP / DISHA feeds via Distributed Lag Non-Linear Models (DLNM).

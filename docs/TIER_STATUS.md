# Data Access Tier Status & Institutional Feasibility Matrix

This document outlines the operational access classification for all data sources considered in SIH26083, providing full transparency on why certain streams are automated in the Tier-1 prototype while others are designed as Tier-2/Tier-3 integration adapters.

---

## Tier Classification Summary

| Tier | Definition | Automation Status in MVP | Human Action Required for Production |
|:---|:---|:---|:---|
| **Tier 1** | Publicly accessible without credentials, human approval, or private agreements | **100% Automated** via REST APIs, static open datasets, and scientific formulas | None (fully reproducible) |
| **Tier 2** | Public/Government services requiring individual registration, API tokens, or specialized protocol handshakes | **Adapter Stubs & Mock Streams Implemented** | Generate API keys / Register user profile |
| **Tier 3** | Restricted institutional datasets, patient health telemetry, municipal confidential records | **Interface Schema Defined; Synthetic Proxy Grounding** | Formal institutional MoU, Ethics approval, MoHFW / Hospital data-sharing agreements |

---

## Source-by-Source Feasibility Analysis

### 1. Tier 1 — Automated MVP Sources

#### NASA POWER API
- **Access Method**: Direct programmatic REST API (`https://power.larc.nasa.gov/api/temporal/daily/point`).
- **Why Tier 1**: Zero credentials required, global coverage, analysis-ready solar irradiance and surface meteorology.
- **Role in MVP**: Powers daily automated meteorological ingestion and 5-day baseline climate trends.
- **Technical Note**: Native resolution is $0.5^\circ \times 0.625^\circ$; used as the macroscopic forcing field.

#### IMD Public Guidance & Bulletins
- **Access Method**: Public web portal (`https://mausam.imd.gov.in/responsive/heatwave_guidance.php`).
- **Why Tier 1**: Official Indian heatwave criteria, color-coded warning definitions, and district bulletins are open public information.
- **Role in MVP**: Calibrates the 4-tier alert scale (Green/Yellow/Orange/Red) and baseline Indian climatological departure definitions.

#### Census of India 2011 Primary Census Abstract (PCA)
- **Access Method**: Open Government Data (OGD) / Census Population Finder.
- **Why Tier 1**: Ward and sub-district level population counts, elderly demographics ($60+$), and worker distributions are published public assets.
- **Role in MVP**: Provides ward-level demographic vulnerability baseline for Ahmedabad and pilot cities.
- **Limitation**: Historical baseline (2011). Documented as static baseline weights rather than 2026 real-time census.

#### Universal Thermal Climate Index (UTCI) Operational Polynomial
- **Access Method**: Standard mathematical polynomial formulation (Bröde et al., 2012; COST Action 730).
- **Why Tier 1**: Open peer-reviewed physics/biometeorology equation.
- **Role in MVP**: Core outdoor physiological thermal stress engine.

#### NIOSH / CDC Wet Bulb Globe Temperature (WBGT) Formulation
- **Access Method**: Open standard equations (NIOSH criteria document 2016-106, Stull 2011).
- **Why Tier 1**: Public scientific standard for occupational thermal strain.
- **Role in MVP**: Occupational worker hazard computation and mandatory rest-schedule generation.

#### NCDC & WHO Public Health Frameworks
- **Access Method**: National Action Plan for Heat-Related Illnesses (NAP-HRI 2024), WHO Heat & Health fact sheets.
- **Why Tier 1**: Standard clinical and disaster management guidelines published by MoHFW and WHO.
- **Role in MVP**: Grounding advisory engine rules for citizens, outdoor laborers, and municipal administrators.

---

## 2. Tier 2 — Account / Configuration Required (Future Production Connectors)

#### NCMRWF NWP GRIB/NetCDF Streams (Unified Model Global & Regional)
- **Access Method**: OpenDAP / RDS server (`https://rds.ncmrwf.gov.in/`).
- **Why Not Tier 1**: High-volume binary forecast streams require institutional registration, IP whitelisting, or academic credentials for automated batch downloads.
- **Human Action Needed**: Team or institutional registration on MoES NCMRWF RDS portal to obtain credentials.
- **Prototype Integration**: `NCMRWFProvider` adapter interface created in `backend/app/data_sources/ncmrwf_stub.py`.

#### ISRO MOSDAC Satellite Products (INSAT-3D/3DR Land Surface Temperature)
- **Access Method**: MOSDAC Open Access REST API with HMAC SHA-256 tokens (`https://www.mosdac.gov.in/`).
- **Why Not Tier 1**: Requires individual registration and account-specific API security tokens.
- **Human Action Needed**: Register on MOSDAC portal and generate secret download token.
- **Prototype Integration**: Architecture document models satellite LST as a spatial urban heat island refinement layer.

#### Copernicus Climate Data Store (CDS) ERA5 / Reanalysis
- **Access Method**: Python `cdsapi` with personal UID and API key.
- **Why Not Tier 1**: Terms of service require personal account login and accepted user agreements.
- **Prototype Integration**: NASA POWER serves as the credential-free Tier-1 equivalent for meteorological variables.

---

## 3. Tier 3 — Institutional & Hospital-Level Datasets (Future Clinical Modeling)

#### NHRIDS / IHIP Patient-Level Heat Stroke Surveillance
- **Access Method**: Integrated Health Information Platform (IHIP) / MoHFW sentinel portal.
- **Why Not Tier 1**: Contains protected health information (PHI), confidential patient records, and restricted hospital admissions data.
- **Human Action Needed**: Formal institutional MoU with MoHFW / National Centre for Disease Control (NCDC), Institutional Review Board (IRB) ethics approval, and state disease surveillance cell authorization.
- **Prototype Integration**: System models health impact as an interpretable **Relative Heat-Health Risk Score (0-100)** rather than fabricating ungrounded clinical death counts.

#### Municipal Hospital Emergency Room & All-Cause Daily Mortality Data
- **Access Method**: Municipal Corporation Vital Statistics / Registrar of Births and Deaths.
- **Why Not Tier 1**: Daily ward-level mortality registries are legally protected and not accessible via open APIs.
- **Prototype Integration**: Relative risk framework designed to plug into Distributed Lag Non-linear Models (DLNM) once institutional mortality time-series are provided in a Phase-2 production deployment.

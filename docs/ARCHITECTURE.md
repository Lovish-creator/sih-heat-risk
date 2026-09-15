# System Architecture — Taapamigo (SIH26083)

**STATUS: SYSTEM ARCHITECTURE SPECIFICATION**

---

## 1. Current Tier-1 Architecture (Working Prototype)

The Tier-1 architecture is designed for transparency, scientific reproducibility, and zero-configuration execution:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             TIER 1 ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Browser Client / UI]                                                      │
│    ├── Vanilla HTML5 / Modern CSS (Custom Design System)                    │
│    ├── Leaflet.js v1.9.4 (Interactive Ward Choropleth)                      │
│    └── Chart.js v4.4.1 (5-Day Trajectory & Telemetry Graphs)                │
│                                │                                            │
│                                ▼  HTTP / REST (JSON)                        │
│  [FastAPI Modular Backend (Python 3.10+)]                                   │
│    ├── Application Router (`backend/app/api/endpoints.py`)                  │
│    │     ├── /api/v1/weather/* (Current & Hourly Series)                    │
│    │     ├── /api/v1/thermal/* (UTCI, WBGT, Heat Index, Hazard)             │
│    │     ├── /api/v1/risk/* (Relative Risk & Duration Factor)               │
│    │     ├── /api/v1/map/risk (GeoJSON FeatureCollection)                   │
│    │     ├── /api/v1/vulnerability/* (Demographics)                         │
│    │     ├── /api/v1/advisory/* (Persona Protocols)                         │
│    │     └── /api/v1/alerts/* (CAP v1.2 Payload)                            │
│    │                                                                        │
│    ├── Scientific Computing Core                                            │
│    │     ├── UTCI Operational Engine (`backend/app/thermal/utci.py`)        │
│    │     ├── WBGT & Stull Engine (`backend/app/thermal/wbgt.py`)            │
│    │     ├── NOAA Heat Index Engine (`backend/app/thermal/heat_index.py`)   │
│    │     ├── Composite Hazard (`backend/app/thermal/hazard.py`)             │
│    │     ├── Demographic Engine (`backend/app/vulnerability/demographic.py`)│
│    │     └── Risk Scoring Engine (`backend/app/risk/engine.py`)             │
│    │                                                                        │
│    ├── GIS & Spatial Management                                             │
│    │     ├── Ward Directory Manager (`backend/app/gis/ward_directory.py`)   │
│    │     ├── 26 Pre-Packaged DataMeet & Delimitation GeoJSON Polygons       │
│    │     └── Stewart & Oke (2012) Local Climate Zone (LCZ) Generator        │
│    │                                                                        │
│    ├── Data Ingestion Layer                                                 │
│    │     ├── Open-Meteo Provider (`backend/app/data_sources/open_meteo.py`) │
│    │     ├── NASA POWER Provider (`backend/app/data_sources/nasa_power.py`) │
│    │     ├── Nominatim Geocoder (`backend/app/data_sources/geocoding.py`)   │
│    │     └── File-Based TTL Cache (`backend/app/data_sources/cache.py`)     │
│    │                                                                        │
│    └── Prototype Persistence & Local Database                               │
│          ├── SQLite Local Database (`data/heat_risk.db`)                    │
│          ├── SQLAlchemy 2.0 ORM (`backend/app/db/models/`)                  │
│          └── CRUD Repositories (`backend/app/db/repositories/`)             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Future Tier-2 / Tier-3 Architecture (Pilot & Production Vision)

**STATUS: FUTURE DESIGN — NOT PART OF CURRENT TIER-1 IMPLEMENTATION**

For future operational pilot expansion (Tier 2) and national production deployment (Tier 3), the architecture will evolve into a distributed, event-driven enterprise system:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FUTURE TIER 2 / TIER 3 ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Institutional Upstream Streams]                                           │
│    ├── MoES / NCMRWF High-Resolution NWP (NCUM 4km Binary GRIB2/NetCDF)     │
│    ├── IMD Automatic Weather Station (AWS) Grid & Radar Telemetry           │
│    ├── ISRO MOSDAC / INSAT-3D Land Surface Temperature (LST) Satellite Feeds│
│    └── MoHFW Integrated Health Information Platform (IHIP Syndromic Feeds)  │
│                                │                                            │
│                                ▼                                            │
│  [Ingestion & Processing Pipeline (Celery / Apache Airflow / Redis)]        │
│    ├── Scheduled NWP Cycle Ingestors (00, 06, 12, 18 UTC)                  │
│    ├── Quality Control, Range Clamping, & Missing Data Imputation           │
│    └── Satellite LST Spatial Downscaling to 100m Urban Canopy Grid          │
│                                │                                            │
│                                ▼                                            │
│  [Operational Storage & GIS Engine]                                         │
│    ├── PostgreSQL 16 + PostGIS Spatial Database                             │
│    ├── TimescaleDB for High-Frequency Sensor Time-Series                    │
│    └── Vector Tile Server (pg_tileserv / GeoServer) for National Scale      │
│                                │                                            │
│                                ▼                                            │
│  [Advanced Modeling & Model Registry Subsystem]                             │
│    ├── Calibrated Distributed Lag Non-linear Models (DLNM)                  │
│    ├── Gradient-Boosted Decision Tree (GBDT) Bias Correction                │
│    └── Model Registry with Continuous Validation & Drift Monitoring         │
│                                │                                            │
│                                ▼                                            │
│  [Multi-Channel Dissemination Engine]                                       │
│    ├── NDMA SACHET Common Alerting Protocol (CAP) Integration               │
│    ├── Automated Telecom SMS / WhatsApp Broadcast Gateways                  │
│    ├── State & District Emergency Operations Center (EOC) Dashboards        │
│    └── Open Government API Gateway (NDSAP Standard)                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

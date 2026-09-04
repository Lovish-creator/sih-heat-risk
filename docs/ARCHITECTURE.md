# SIH26083 - System Architecture & Technical Specification

**Extreme Heatwave Early Warning and Human Thermal Stress Index**
**Organization:** Ministry of Earth Sciences (MoES) / National Centre for Medium Range Weather Forecasting (NCMRWF)

---

## 1. Executive Summary
The SIH26083 platform transitions heatwave disaster management from monitoring simple dry-bulb atmospheric temperature to quantifying **"What the weather will do to humans"**. By coupling multi-parameter atmospheric forcing (temperature, humidity, wind velocity, and solar shortwave irradiance) with human biometeorological energy balance models (UTCI, WBGT, Heat Index) and Census demographic vulnerability, the platform generates localized **Ward-Level Relative Heat-Health Risk Scores (0–100)** and automated, persona-tailored public health advisories across a 5-day forecast horizon.

---

## 2. Problem Interpretation & Domain Boundary
Conventional heatwave alerts in India (e.g., $T_{\max} \ge 40^\circ\text{C}$ or $+4.5^\circ\text{C}$ departure from normal) suffer from two fundamental operational shortcomings:
1. **The Thermoregulatory Blindspot**: A dry, windy $40^\circ\text{C}$ day allows evaporative sweat cooling, resulting in manageable physiological stress ($\text{UTCI} \approx 35^\circ\text{C}$), whereas a humid, stagnant, high-radiation $40^\circ\text{C}$ day cripples evaporative heat dissipation, triggering lethal heat strain ($\text{UTCI} > 48^\circ\text{C}$, Extreme Heat Stress).
2. **Homogeneous Risk Assumption**: Blanket district-wide alerts ignore intra-urban demographic disparities. Wards with dense elderly populations ($60+$) and high concentrations of outdoor informal laborers face exponentially higher heat stroke morbidity than commercial zones.

SIH26083 solves both challenges through an interpretable, reproducible Tier-1 pipeline.

---

## 3. Required Architectural Diagrams

### Diagram 1 — System Architecture
```mermaid
graph TB
    subgraph External_Data_Sources [Authoritative Tier-1 Data Streams]
        NASA[NASA POWER API - Met & Solar]
        IMD[IMD Guidance & Norms]
        CENSUS[Census 2011 PCA Data]
        GEO[Municipal GeoJSON Polygons]
    end

    subgraph Ingestion_Layer [Ingestion, Caching & Normalization]
        ADAPTER[WeatherProvider Adapter]
        CACHE[(Local File/SQLite Cache)]
        VULN_ING[Demographic Pipeline]
    end

    subgraph Scientific_Compute_Core [Biometeorological & Risk Core]
        UTCI_E[UTCI 6th-Order Polynomial Engine]
        WBGT_E[NIOSH WBGT Liljegren Engine]
        HI_E[Rothfusz Heat Index Engine]
        HAZARD_E[Thermal Hazard Normalizer]
        VULN_E[Vulnerability Index Engine]
        RISK_E[Human Heat-Health Risk Engine]
        ADV_E[NCDC/WHO Actionable Advisory Engine]
    end

    subgraph Spatial_Service_Layer [Spatial Attribution & Services]
        GIS_E[GIS Ward Attribution Engine]
        FORECAST_E[5-Day Horizon Aggregator]
    end

    subgraph API_Delivery [FastAPI REST Endpoints]
        API_GATEWAY[FastAPI Gateway / OpenAPI Docs]
    end

    subgraph Presentation_Layer [Client Application]
        UI[Interactive Web Dashboard]
        MAP[Leaflet Choropleth Map]
        CHART[Chart.js Horizon Visualizer]
        ADVISORY_BOX[Persona Action Cards]
    end

    NASA --> ADAPTER
    IMD --> ADAPTER
    CENSUS --> VULN_ING
    GEO --> GIS_E
    ADAPTER <--> CACHE

    ADAPTER --> UTCI_E & WBGT_E & HI_E
    UTCI_E & WBGT_E & HI_E --> HAZARD_E
    VULN_ING --> VULN_E

    HAZARD_E --> RISK_E
    VULN_E --> RISK_E
    RISK_E --> GIS_E & ADV_E & FORECAST_E

    GIS_E & ADV_E & FORECAST_E --> API_GATEWAY
    API_GATEWAY --> UI
    UI --> MAP & CHART & ADVISORY_BOX
```

---

### Diagram 2 — End-to-End Data Flow
```mermaid
sequenceDiagram
    autonumber
    actor Client as User / Dashboard
    participant API as FastAPI Backend
    participant WP as WeatherProvider
    participant Cache as Response Cache
    participant Ext as NASA POWER / IMD
    participant Sci as Thermal & Risk Engine
    participant GIS as GIS Attribution Engine

    Client->>API: GET /api/v1/risk/forecast?city=ahmedabad
    API->>WP: fetch_forecast_data(city, days=5)
    WP->>Cache: check_cache(city, date_range)
    alt Cache Hit
        Cache-->>WP: return cached_raw_payload
    else Cache Miss / Expired
        WP->>Ext: HTTP GET NASA POWER API
        Ext-->>WP: return JSON {T2M, RH2M, WS10M, ALLSKY_SFC_SW_DWN}
        WP->>Cache: store_cache(city, raw_payload)
    end
    WP-->>API: normalized_weather_series
    API->>Sci: compute_thermal_hazard(weather_series)
    Sci->>Sci: calculate UTCI, WBGT, Heat Index
    Sci->>Sci: evaluate Hazard Score (0-100)
    API->>Sci: evaluate_risk(hazard, vulnerability, duration)
    Sci-->>API: risk_scores_series
    API->>GIS: join_ward_attribution(risk_scores, city_geojson)
    GIS-->>API: enriched_ward_geojson
    API-->>Client: HTTP 200 JSON {horizon, wards, advisories, provenance}
```

---

### Diagram 3 — Thermal Stress Engine
```mermaid
graph LR
    subgraph Inputs [Meteorological Forcing Variables]
        T[Air Temp T2M °C]
        RH[Relative Humidity RH2M %]
        WS[10m Wind Speed WS10M m/s]
        RAD[Solar Irradiance ALLSKY W/m²]
    end

    subgraph Derivations [Intermediate Variables]
        VP[Vapor Pressure e hPa - Magnus]
        MRT[Mean Radiant Temp Tmrt °C]
        WB[Wet Bulb Temp Tw °C - Stull]
        BG[Black Globe Temp Tg °C]
    end

    subgraph Models [Biometeorological Indices]
        UTCI[UTCI 6th-Order Polynomial]
        WBGT[NIOSH WBGT Outdoor]
        HI[Rothfusz Heat Index]
    end

    subgraph Output [Hazard Quantification]
        HAZARD[Thermal Hazard Score: 0 - 100]
    end

    T & RH --> VP
    T & RAD & WS --> MRT
    T & RH --> WB
    T & RAD & WS --> BG

    T & VP & WS & MRT --> UTCI
    WB & BG & T --> WBGT
    T & RH --> HI

    UTCI -->|60% Weight| HAZARD
    WBGT -->|25% Weight| HAZARD
    HI -->|15% Weight| HAZARD
```

---

### Diagram 4 — Vulnerability Engine
```mermaid
graph TD
    subgraph Census_Input [Census of India 2011 Primary Census Abstract]
        TOT[Total Population]
        ELD[Population Aged >= 60 Years]
        WRK[Main & Marginal Outdoor Workers]
        AREA[Ward Geometric Area km²]
    end

    subgraph Indicators [Demographic Sensitivity Ratios]
        R_ELD["Elderly Ratio = ELD / TOT"]
        R_WRK["Outdoor Worker Ratio = WRK / TOT"]
        DENS["Density = TOT / AREA"]
    end

    subgraph Normalization [Min-Max Scaling 0 - 100]
        N_ELD[Normalized Elderly Score]
        N_WRK[Normalized Worker Score]
        N_DENS[Normalized Density Score]
    end

    subgraph Vulnerability_Output [Composite Vulnerability]
        V_SCORE["Vulnerability Score = (0.40 * N_ELD) + (0.35 * N_WRK) + (0.25 * N_DENS)"]
    end

    TOT & ELD --> R_ELD
    TOT & WRK --> R_WRK
    TOT & AREA --> DENS

    R_ELD --> N_ELD
    R_WRK --> N_WRK
    DENS --> N_DENS

    N_ELD & N_WRK & N_DENS --> V_SCORE
```

---

### Diagram 5 — Risk Engine
```mermaid
graph TD
    HAZARD[Thermal Hazard Score 0-100]
    VULN[Demographic Vulnerability Score 0-100]
    DUR[Consecutive Heatwave Duration Factor 0-1]

    subgraph Risk_Computation [Multi-Criteria Composite Formula]
        FORMULA["Heat Risk Score = (0.55 * Hazard) + (0.30 * Vulnerability) + (0.15 * DurationFactor * 100)"]
    end

    subgraph Classification [IMD-Aligned 4-Tier Alert Levels]
        GREEN[GREEN: Normal 0 - 25]
        YELLOW[YELLOW: Watch 26 - 50]
        ORANGE[ORANGE: Alert 51 - 75]
        RED[RED: Warning 76 - 100]
    end

    HAZARD --> FORMULA
    VULN --> FORMULA
    DUR --> FORMULA

    FORMULA --> GREEN & YELLOW & ORANGE & RED
```

---

### Diagram 6 — GIS Flow
```mermaid
graph LR
    MET_GRID[Regional Weather Grid ~50km] --> SPATIAL_MAP[Spatial Attribution Mapper]
    WARD_BOUNDS[Municipal Ward GeoJSON Boundaries] --> SPATIAL_MAP
    WARD_CENSUS[Ward Demographic Vulnerability] --> SPATIAL_MAP

    SPATIAL_MAP --> WARD_RISK[Ward-Level Risk Attribution GeoJSON]
    WARD_RISK --> CHOROPLETH[Leaflet Thematic Choropleth Layer]

    note["Transparent Note: Ward Risk Attribution joins regional hazard with localized vulnerability; does not claim micro-scale meteorological resolution."] -.-> SPATIAL_MAP
```

---

### Diagram 7 — API Architecture
```mermaid
graph TD
    subgraph Client_App [Client Applications]
        WEB[Web Dashboard]
        CLI[Python CLI / Scripts]
        THIRD_PARTY[External Alert Consumers]
    end

    subgraph FastAPI_Backend [FastAPI Application Framework]
        ROUTER[API Router / OpenAPI]
        HEALTH_EP["/health & /api/v1/data-status"]
        WEATHER_EP["/api/v1/weather/*"]
        THERMAL_EP["/api/v1/thermal/*"]
        RISK_EP["/api/v1/risk/* & /api/v1/map/risk"]
        ADV_EP["/api/v1/advisory"]
        SRC_EP["/api/v1/sources & /api/v1/methodology"]
    end

    subgraph Internal_Services [Service Layer]
        WP_SVC[Weather Service]
        TH_SVC[Thermal Service]
        RSK_SVC[Risk Service]
        GIS_SVC[GIS Service]
        ADV_SVC[Advisory Service]
    end

    subgraph Storage [Data Cache & GeoJSON]
        CACHE_STORE[(SQLite / JSON File Cache)]
        GEO_STORE[(Local GeoJSON Repository)]
    end

    WEB & CLI & THIRD_PARTY --> ROUTER
    ROUTER --> HEALTH_EP & WEATHER_EP & THERMAL_EP & RISK_EP & ADV_EP & SRC_EP

    WEATHER_EP --> WP_SVC
    THERMAL_EP --> TH_SVC
    RISK_EP --> RSK_SVC & GIS_SVC
    ADV_EP --> ADV_SVC

    WP_SVC <--> CACHE_STORE
    GIS_SVC <--> GEO_STORE
```

---

### Diagram 8 — Deployment Architecture
```mermaid
graph TD
    subgraph User_Environment [Client Device]
        BROWSER[Modern Web Browser - HTML5/CSS3/JS]
    end

    subgraph Host_Container [Docker / Local Host OS]
        UVICORN[Uvicorn ASGI Server]
        FASTAPI_APP[FastAPI Python 3.11 Runtime]
        STATIC_FILES[Static UI Asset Server]
        LOCAL_CACHE[(Data Cache & GeoJSON Files)]
    end

    subgraph Upstream_APIs [Public Tier-1 Providers]
        NASA_API[NASA POWER REST API]
        IMD_PORTAL[IMD Public Guidance]
    end

    BROWSER -->|HTTP Port 8000| UVICORN
    UVICORN --> FASTAPI_APP
    FASTAPI_APP --> STATIC_FILES
    FASTAPI_APP <--> LOCAL_CACHE
    FASTAPI_APP -->|HTTPS REST| NASA_API & IMD_PORTAL
```

---

### Diagram 9 — SIH Requirement Mapping
```mermaid
graph TD
    subgraph SIH26083_Requirements [Official Problem Statement Requirements]
        R1[Human Thermal Stress Index]
        R2[Temp + Humidity + Wind + Radiation]
        R3[UTCI / WBGT / Heat Index]
        R4[Localized 3-5 Day Forecast Anticipation]
        R5[Demographic Vulnerability: Elderly & Outdoor Workers]
        R6[GIS Mapping & Ward-Level Risk]
        R7[Actionable Public Health Advisories]
        R8[Relative Mortality/Health Risk Concept]
    end

    subgraph Implementation_Modules [SIH26083 System Modules]
        M1[backend/app/thermal/hazard.py]
        M2[backend/app/thermal/utci.py & wbgt.py]
        M3[backend/app/data_sources/nasa_power.py]
        M4[backend/app/vulnerability/demographic.py]
        M5[backend/app/gis/engine.py & frontend/map.js]
        M6[backend/app/advisory/engine.py]
        M7[backend/app/risk/engine.py]
    end

    R1 & R2 --> M1 & M2
    R3 --> M2
    R4 --> M3
    R5 --> M4
    R6 --> M5
    R7 --> M6
    R8 --> M7
```

---

## 4. Functional & Non-Functional Specifications
- **Response Latency**: $< 200\text{ ms}$ for cached/GIS endpoints, $< 1.5\text{ s}$ for live NASA POWER fetches.
- **Reproducibility**: Zero proprietary API keys required. Out-of-the-box demo mode (`DEMO_MODE=true`) guarantees 100% deterministic execution during hackathon presentations.
- **Extensibility**: Clean object-oriented provider abstraction (`WeatherProvider`) allowing one-line plug-in of future NCMRWF GRIB2 or ISRO MOSDAC satellite decoders.

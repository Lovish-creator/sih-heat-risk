# SIH26083 REST API Specification

The SIH26083 backend exposes 14 REST endpoints adhering to the OpenAPI 3.0 specification. Interactive Swagger UI is accessible at `http://localhost:8000/docs` and ReDoc at `http://localhost:8000/redoc`.

---

## 1. System & Observability Endpoints

### `GET /health`
Returns the operational health and readiness of the service.
- **Response `200 OK`**:
```json
{
  "status": "healthy",
  "app_name": "SIH26083-Heat-Risk-Early-Warning",
  "version": "1.0.0",
  "demo_mode": true,
  "timestamp": "2026-09-05T00:00:00Z"
}
```

### `GET /api/v1/data-status`
Returns cache telemetry, data freshness, upstream API connectivity, and active city profiles.
- **Response `200 OK`**:
```json
{
  "active_city": "ahmedabad",
  "demo_mode": true,
  "cache_entries": 12,
  "latest_ingestion_timestamp": "2026-09-05T00:00:00Z",
  "upstream_sources": {
    "nasa_power": "ONLINE",
    "imd_guidance": "ONLINE",
    "census_2011": "LOADED"
  }
}
```

---

## 2. Spatial & Location Endpoints

### `GET /api/v1/locations`
Returns the list of configured Indian cities and their geographic bounding boxes.
- **Response `200 OK`**:
```json
{
  "cities": [
    {
      "id": "ahmedabad",
      "name": "Ahmedabad",
      "state": "Gujarat",
      "region_type": "plains",
      "center": {"lat": 23.0225, "lon": 72.5714},
      "is_pilot": true
    }
  ]
}
```

---

## 3. Meteorological & Thermal Endpoints

### `GET /api/v1/weather/current?city=ahmedabad`
Returns current dry-bulb temperature, relative humidity, wind speed, and solar irradiance.

### `GET /api/v1/weather/forecast?city=ahmedabad&days=5`
Returns 5-day daily forecast meteorological series (D+1 to D+5).

### `GET /api/v1/thermal/current?city=ahmedabad`
Returns calculated biometeorological indices (UTCI, WBGT, Heat Index, Vapor Pressure, $T_{mrt}$) and thermal stress categories.

### `GET /api/v1/thermal/forecast?city=ahmedabad&days=5`
Returns 5-day daily thermal stress metrics, comparing raw air temperature against physiological UTCI and occupational WBGT.

---

## 4. Vulnerability & Risk Endpoints

### `GET /api/v1/vulnerability?city=ahmedabad`
Returns Census 2011 baseline demographic indicators across all municipal wards (total population, elderly $60+$ ratio, outdoor worker ratio, population density, normalized vulnerability score).

### `GET /api/v1/risk/current?city=ahmedabad`
Returns city-wide composite Heat-Health Risk Score (0–100), alert level (Green/Yellow/Orange/Red), and driver breakdown.

### `GET /api/v1/risk/forecast?city=ahmedabad&days=5`
Returns 5-day composite risk trajectory incorporating cumulative heatwave duration penalties.

### `GET /api/v1/map/risk?city=ahmedabad&day=1`
Returns enriched GeoJSON feature collection containing ward boundaries, demographic indices, environmental hazard scores, composite risk scores, and alert color codes for Leaflet rendering.

---

## 5. Advisory & Provenance Endpoints

### `GET /api/v1/advisory?city=ahmedabad&risk_level=ORANGE`
Returns persona-tailored public health advisories grounded in NCDC 2024 and WHO guidelines for:
1. Citizens (`general_public`)
2. Outdoor Workers (`outdoor_workers` with NIOSH work-rest cycles)
3. Municipal Authorities (`authorities` with cooling logistics)

### `GET /api/v1/sources`
Returns the complete `data/SOURCE_REGISTRY.md` metadata in JSON format.

### `GET /api/v1/methodology`
Returns scientific equations, parameters, and references for UTCI, WBGT, Heat Index, and Risk scoring.

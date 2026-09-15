# REST API Specification — Taapamigo (SIH26083)

**Base URL:** `http://127.0.0.1:8000`  
**API Version:** `v1` (`/api/v1/`)  
**Interactive Swagger UI:** `http://127.0.0.1:8000/docs`  
**ReDoc Specification:** `http://127.0.0.1:8000/redoc`

---

## 1. System & Operational Observability

### 1.1 `GET /health`
Returns the operational health, database connectivity, and environment status.

- **Request:** `GET /health`
- **Response `200 OK`**:
```json
{
  "status": "healthy",
  "app_name": "Taapamigo - Extreme Heat Early Warning",
  "version": "1.2.0-modular",
  "environment": "development",
  "data_mode": "hybrid",
  "database": "connected (sqlite)",
  "timestamp": "2026-09-12T17:00:00.000Z"
}
```

---

### 1.2 `GET /api/v1/data-freshness`
Returns real-time telemetry freshness, active data sources, and background ingestion health.

- **Request:** `GET /api/v1/data-freshness`
- **Response `200 OK`**:
```json
{
  "status": "ok",
  "timestamp": "2026-09-12T17:00:00.000Z",
  "data_mode": "hybrid",
  "total_locations": 18,
  "total_wards_seeded": 1145,
  "upstream_sources": {
    "open_meteo": "ONLINE",
    "nasa_power": "ONLINE",
    "census_2011": "LOADED"
  },
  "provenance_policy": "Strict Open Provenance - Generated geometries explicitly flagged"
}
```

---

## 2. Locations and Spatial Wards

### 2.1 `GET /api/v1/locations`
Returns all registered Indian municipal corporations and benchmark cities.

- **Request:** `GET /api/v1/locations`
- **Response `200 OK`**:
```json
[
  {
    "id": "abohar",
    "name": "Abohar",
    "state": "Punjab",
    "latitude": 30.145,
    "longitude": 74.199,
    "elevation": 185.0,
    "is_pilot": true,
    "ward_count": 50
  },
  {
    "id": "ahmedabad",
    "name": "Ahmedabad",
    "state": "Gujarat",
    "latitude": 23.0225,
    "longitude": 72.5714,
    "elevation": 53.0,
    "is_pilot": true,
    "ward_count": 48
  }
]
```

---

### 2.2 `GET /api/v1/wards`
Returns municipal wards and zones for a given city, including boundary provenance and census indicators.

- **Request:** `GET /api/v1/wards?city=abohar`
- **Query Parameters:**
  - `city` (string, required): City slug (e.g., `abohar`, `delhi`, `mumbai`)
- **Response `200 OK`**:
```json
{
  "city": "abohar",
  "ward_count": 50,
  "provenance": {
    "is_official_geometry": false,
    "is_generated_geometry": true,
    "geometry_source": "census_density_proportional_v1",
    "demographics_source": "Census of India 2011 PCA"
  },
  "wards": [
    {
      "id": "abohar-w01",
      "ward_number": 1,
      "name": "Ward 1 - Circular Road",
      "zone_name": "Central Zone",
      "centroid": {"lat": 30.1452, "lon": 74.1988},
      "area_sqkm": 0.84,
      "demographics": {
        "total_population": 4200,
        "population_density": 5000.0,
        "elderly_percentage": 11.2,
        "outdoor_worker_pct": 34.5,
        "vulnerability_score": 58.4
      }
    }
  ]
}
```

---

## 3. Atmospheric & Thermal Stress Endpoints

### 3.1 `GET /api/v1/weather/current`
Returns current surface atmospheric telemetry.

- **Request:** `GET /api/v1/weather/current?city=abohar`
- **Response `200 OK`**:
```json
{
  "city": "abohar",
  "timestamp": "2026-09-12T17:00:00.000Z",
  "temperature_celsius": 41.2,
  "relative_humidity": 48.0,
  "dew_point_celsius": 28.1,
  "wind_speed_ms": 2.4,
  "solar_radiation_wm2": 780.0,
  "surface_pressure_hpa": 1004.2,
  "data_source": "open-meteo",
  "is_fallback": false,
  "fallback_reason": null
}
```

---

### 3.2 `GET /api/v1/thermal/current`
Calculates physiological thermal stress indices (UTCI, WBGT, Heat Index).

- **Request:** `GET /api/v1/thermal/current?city=abohar`
- **Response `200 OK`**:
```json
{
  "city": "abohar",
  "timestamp": "2026-09-12T17:00:00.000Z",
  "engine_version": "1.2.0-scientific",
  "meteorology": {
    "air_temperature": 41.2,
    "relative_humidity": 48.0,
    "wind_speed_10m": 2.4,
    "solar_radiation": 780.0
  },
  "indices": {
    "utci_celsius": 47.8,
    "utci_category": "Extreme Heat Stress",
    "wbgt_celsius": 32.4,
    "wbgt_flag": "Black Flag",
    "heat_index_celsius": 52.1,
    "heat_index_category": "Extreme Danger",
    "mean_radiant_temperature": 61.2
  },
  "thermal_hazard_score": 88.5
}
```

---

## 4. Relative Heat-Health Risk & GIS choropleth

### 4.1 `GET /api/v1/risk/current`
Returns the composite relative heat-health risk assessment across all city wards.

- **Request:** `GET /api/v1/risk/current?city=abohar`
- **Response `200 OK`**:
```json
{
  "city": "abohar",
  "timestamp": "2026-09-12T17:00:00.000Z",
  "city_risk_score": 74.2,
  "city_risk_category": "High Risk",
  "model_version": "RiskEngine-TriFactor-v1.2.0",
  "weights": {
    "thermal_hazard": 0.60,
    "vulnerability": 0.40,
    "persistence_factor": 1.05
  },
  "disclaimer": "Relative spatial prioritization score for early warning; does not predict clinical mortality.",
  "ward_assessments": [
    {
      "ward_id": "abohar-w01",
      "ward_name": "Ward 1 - Circular Road",
      "risk_score": 78.4,
      "risk_category": "Extreme Risk",
      "color_hex": "#b91c1c",
      "breakdown": {
        "thermal_hazard": 88.5,
        "demographic_vulnerability": 58.4,
        "persistence_multiplier": 1.05
      }
    }
  ]
}
```

---

### 4.2 `GET /api/v1/map/risk`
Returns valid GeoJSON FeatureCollection with embedded risk styling for Leaflet / Mapbox.

- **Request:** `GET /api/v1/map/risk?city=abohar`
- **Response `200 OK`**:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "abohar-w01",
      "properties": {
        "ward_id": "abohar-w01",
        "ward_name": "Ward 1 - Circular Road",
        "risk_score": 78.4,
        "risk_category": "Extreme Risk",
        "fillColor": "#b91c1c",
        "fillOpacity": 0.7,
        "population": 4200,
        "elderly_pct": 11.2,
        "outdoor_worker_pct": 34.5
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[74.195, 30.142], [74.202, 30.142], [74.202, 30.148], [74.195, 30.148], [74.195, 30.142]]]
      }
    }
  ]
}
```

---

## 5. Advisories & Alert Dispatch

### 5.1 `GET /api/v1/advisories`
Returns persona-tailored public health guidance.

- **Request:** `GET /api/v1/advisories?city=abohar&persona=outdoor_workers`
- **Query Parameters:**
  - `city` (string, required)
  - `persona` (string, optional): `general_public`, `outdoor_workers`, `elderly_caregivers`, `municipal_officials`
- **Response `200 OK`**:
```json
{
  "city": "abohar",
  "risk_category": "Extreme Risk",
  "persona": "outdoor_workers",
  "headline": "RED ALERT: Suspend Non-Essential Strenuous Outdoor Labor",
  "hydration_guideline": "Consume 1.0 Liter of water or ORS solution per hour in small, frequent intervals.",
  "work_rest_regimen": "15 minutes light work / 45 minutes shaded rest per hour (NIOSH Criteria).",
  "clinical_citations": ["NCDC National Action Plan on Heat-Related Illnesses 2024", "ISO 7243:2017"]
}
```

---

### 5.2 `POST /api/v1/alerts/test`
Dispatches a simulated Common Alerting Protocol (CAP) payload.

- **Request:** `POST /api/v1/alerts/test`
```json
{
  "city": "abohar",
  "alert_level": "RED",
  "channel": "cap_json"
}
```
- **Response `200 OK`**:
```json
{
  "dispatch_id": "cap-9f8e7d6c-5b4a-3210",
  "status": "mock_logged",
  "channel": "cap_json",
  "payload": {
    "identifier": "TAAPAMIGO-ABOHAR-20260912-001",
    "sender": "taapamigo-alert-engine@sih26083.gov.in",
    "status": "Actual",
    "msgType": "Alert",
    "scope": "Public",
    "info": {
      "category": "Met",
      "event": "Extreme Thermal Stress Heatwave",
      "urgency": "Immediate",
      "severity": "Extreme",
      "certainty": "Observed",
      "headline": "Extreme Heatwave Danger in Abohar - Universal Thermal Stress Alert",
      "description": "UTCI has exceeded 46°C with WBGT > 32°C. High risk of exertional heat stroke."
    }
  }
}
```

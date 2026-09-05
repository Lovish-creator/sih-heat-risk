"""
Integration tests for FastAPI REST Endpoints.
"""

import pytest
import sys
import os
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data


def test_data_status_endpoint():
    response = client.get("/api/v1/data-status?city=ahmedabad")
    assert response.status_code == 200
    data = response.json()
    assert "upstream_sources" in data
    assert data["active_city"] == "Ahmedabad"


def test_locations_endpoint():
    response = client.get("/api/v1/locations")
    assert response.status_code == 200
    data = response.json()
    assert "cities" in data
    assert len(data["cities"]) >= 1
    assert any(c["id"] == "ahmedabad" for c in data["cities"])


def test_weather_endpoints():
    # Current weather
    res_curr = client.get("/api/v1/weather/current?city=ahmedabad")
    assert res_curr.status_code == 200
    curr_data = res_curr.json()
    assert "weather" in curr_data
    assert "temp_c" in curr_data["weather"]

    # Forecast weather
    res_fc = client.get("/api/v1/weather/forecast?city=ahmedabad&days=5")
    assert res_fc.status_code == 200
    fc_data = res_fc.json()
    assert len(fc_data["data"]) == 5


def test_thermal_endpoints():
    # Current thermal
    res_th = client.get("/api/v1/thermal/current?city=ahmedabad")
    assert res_th.status_code == 200
    th_data = res_th.json()
    assert "thermal_analysis" in th_data
    assert "utci" in th_data["thermal_analysis"]["metrics"]
    assert "wbgt" in th_data["thermal_analysis"]["metrics"]

    # Forecast thermal
    res_th_fc = client.get("/api/v1/thermal/forecast?city=ahmedabad&days=5")
    assert res_th_fc.status_code == 200
    assert len(res_th_fc.json()["series"]) == 5


def test_vulnerability_endpoint():
    response = client.get("/api/v1/vulnerability?city=ahmedabad")
    assert response.status_code == 200
    data = response.json()
    assert data["total_wards"] == 20
    assert len(data["wards"]) == 20


def test_risk_endpoints():
    # Current risk
    res_r = client.get("/api/v1/risk/current?city=ahmedabad")
    assert res_r.status_code == 200
    r_data = res_r.json()
    assert "heat_risk_score" in r_data
    assert "alert_level" in r_data

    # Forecast risk
    res_r_fc = client.get("/api/v1/risk/forecast?city=ahmedabad&days=5")
    assert res_r_fc.status_code == 200
    assert len(res_r_fc.json()["horizon"]) == 5


def test_map_risk_endpoint():
    response = client.get("/api/v1/map/risk?city=ahmedabad&day=1")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) == 20


def test_advisory_endpoint():
    response = client.get("/api/v1/advisory?city=ahmedabad&alert_level=ORANGE")
    assert response.status_code == 200
    data = response.json()
    assert "personas" in data
    assert "general_public" in data["personas"]
    assert "outdoor_workers" in data["personas"]
    assert "authorities" in data["personas"]


def test_provenance_and_methodology_endpoints():
    res_src = client.get("/api/v1/sources")
    assert res_src.status_code == 200
    assert res_src.json()["total_registered_sources"] >= 10

    res_meth = client.get("/api/v1/methodology")
    assert res_meth.status_code == 200
    assert "models" in res_meth.json()


def test_thermal_calculate_post_endpoint():
    # Test POST /api/v1/thermal/calculate
    payload = {
        "temp_c": 42.0,
        "relative_humidity_pct": 35.0,
        "wind_speed_10m_m_s": 2.0,
        "solar_radiation_w_m2": 700.0
    }
    res = client.post("/api/v1/thermal/calculate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    hazard = data["hazard_analysis"]
    assert "utci" in hazard["metrics"]
    assert "wbgt" in hazard["metrics"]
    assert "heat_index" in hazard["metrics"]
    assert hazard["metrics"]["utci"]["value_c"] > 35.0
    assert hazard["composite_hazard_score"] > 50.0


def test_dynamic_coordinates_risk_and_census():
    # Test coordinates for Pune (18.5204, 73.8567)
    res = client.get("/api/v1/risk/current?lat=18.5204&lon=73.8567")
    assert res.status_code == 200
    data = res.json()
    assert "heat_risk_score" in data
    assert data["city_name"] != ""

    # Test map risk for detected coordinates
    map_res = client.get("/api/v1/map/risk?lat=18.5204&lon=73.8567&day=1")
    assert map_res.status_code == 200
    map_data = map_res.json()
    assert map_data["type"] == "FeatureCollection"
    assert len(map_data["features"]) >= 1
    props = map_data["features"][0]["properties"]
    assert "demographics" in props
    assert props["demographics"]["tot_pop"] > 0


def test_calculations_reference_endpoint():
    res = client.get("/api/v1/calculations/reference")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "markdown_content" in data
    assert "Universal Thermal Climate Index" in data["markdown_content"]
    assert "calculations_verifier.py" in data["verifier_script"]



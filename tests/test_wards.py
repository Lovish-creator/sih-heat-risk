"""
Unit tests for Municipal Ward Manager and 50-Ward Spatial Risk Engine.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.gis.ward_directory import MunicipalWardManager


def test_abohar_50_wards_generation():
    manager = MunicipalWardManager()
    weather = {
        "temp_c": 43.0,
        "relative_humidity_pct": 30.0,
        "wind_speed_10m_m_s": 2.0,
        "solar_radiation_w_m2": 750.0
    }

    result = manager.generate_ward_risk_collection("abohar", weather, consecutive_heat_days=2)
    assert result["type"] == "FeatureCollection"
    features = result["features"]
    
    # Assert exactly 50 wards
    assert len(features) == 50, f"Expected 50 wards for Abohar, got {len(features)}"

    # Verify geometries and properties
    for idx, f in enumerate(features, 1):
        assert f["type"] == "Feature"
        assert f["geometry"]["type"] == "Polygon"
        assert len(f["geometry"]["coordinates"][0]) >= 5
        p = f["properties"]
        assert p["ward_number"] == idx
        assert "heat_risk_score" in p
        assert 0.0 <= p["heat_risk_score"] <= 100.0
        assert p["alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
        assert p["alert_color"] in ["#10b981", "#f59e0b", "#f97316", "#ef4444", "#fd7e14", "#dc3545", "#28a745", "#ffc107"]
        assert "demographics" in p
        assert p["demographics"]["tot_pop"] > 0
        assert p["demographics"]["outdoor_worker_percentage"] > 0
        assert p["demographics"]["elderly_percentage"] > 0
        assert p["utci_val"] > 0.0
        assert p["wbgt_val"] > 0.0


def test_ahmedabad_48_wards_and_mumbai_24_wards():
    manager = MunicipalWardManager()
    weather = {
        "temp_c": 41.0,
        "relative_humidity_pct": 40.0,
        "wind_speed_10m_m_s": 2.5,
        "solar_radiation_w_m2": 700.0
    }

    ahm = manager.generate_ward_risk_collection("ahmedabad", weather)
    assert len(ahm["features"]) == 48

    mum = manager.generate_ward_risk_collection("mumbai", weather)
    assert len(mum["features"]) == 24


def test_arbitrary_town_dynamic_50_wards():
    manager = MunicipalWardManager()
    weather = {
        "temp_c": 39.0,
        "relative_humidity_pct": 50.0,
        "wind_speed_10m_m_s": 1.5,
        "solar_radiation_w_m2": 650.0
    }

    # Test an arbitrary town like Fazilka, Bathinda, or Alwar
    dyn = manager.generate_ward_risk_collection("fazilka", weather, custom_lat=30.4042, custom_lon=74.0270)
    assert len(dyn["features"]) == 50
    assert dyn["metadata"]["city_name"] != ""
    assert dyn["metadata"]["total_wards"] == 50

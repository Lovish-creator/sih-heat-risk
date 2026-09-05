"""
Unit tests for Municipal Ward Manager, Pan-India Coverage, and Real-Size Ward Geometry Engine.
"""

import pytest
import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.gis.ward_directory import MunicipalWardManager


def test_abohar_50_wards_generation_and_real_size():
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
    areas = []
    for idx, f in enumerate(features, 1):
        assert f["type"] == "Feature"
        assert f["geometry"]["type"] == "Polygon"
        coords = f["geometry"]["coordinates"][0]
        assert len(coords) == 5
        # Verify polygon closed
        assert coords[0] == coords[-1]

        p = f["properties"]
        assert p["ward_number"] == idx
        assert "heat_risk_score" in p
        assert 0.0 <= p["heat_risk_score"] <= 100.0
        assert p["alert_level"] in ["GREEN", "YELLOW", "ORANGE", "RED"]
        assert p["alert_color"] in ["#10b981", "#f59e0b", "#f97316", "#ef4444", "#fd7e14", "#dc3545", "#28a745", "#ffc107"]
        assert "lcz_class" in p
        assert "LCZ" in p["lcz_class"]
        assert "uhi_delta_c" in p

        d = p["demographics"]
        assert d["tot_pop"] > 0
        assert d["outdoor_worker_percentage"] > 0
        assert d["elderly_percentage"] > 0
        assert d["area_sqkm"] > 0.0
        assert d["area_hectares"] == round(d["area_sqkm"] * 100.0, 1)
        assert d["pop_density_per_sqkm"] > 0.0
        assert p["utci_val"] > 0.0
        assert p["wbgt_val"] > 0.0

        areas.append(d["area_sqkm"])

    # Verify that inner core wards (first 10) have smaller area than outer fringe wards (last 10)
    avg_inner_area = sum(areas[:10]) / 10.0
    avg_outer_area = sum(areas[-10:]) / 10.0
    assert avg_inner_area < avg_outer_area, f"Inner area {avg_inner_area} should be smaller than outer area {avg_outer_area}"


def test_pan_india_major_cities():
    manager = MunicipalWardManager()
    weather = {
        "temp_c": 41.0,
        "relative_humidity_pct": 40.0,
        "wind_speed_10m_m_s": 2.5,
        "solar_radiation_w_m2": 700.0
    }

    # Test Ahmedabad (48 wards)
    ahm = manager.generate_ward_risk_collection("ahmedabad", weather)
    assert len(ahm["features"]) == 48

    # Test Mumbai (24 wards)
    mum = manager.generate_ward_risk_collection("mumbai", weather)
    assert len(mum["features"]) == 24

    # Test Delhi (50 wards)
    delhi = manager.generate_ward_risk_collection("delhi", weather)
    assert len(delhi["features"]) == 50

    # Test Bengaluru (60 wards)
    blr = manager.generate_ward_risk_collection("bengaluru", weather)
    assert len(blr["features"]) == 60

    # Test Chennai (60 wards)
    chn = manager.generate_ward_risk_collection("chennai", weather)
    assert len(chn["features"]) == 60

    # Test Kolkata (60 wards)
    kol = manager.generate_ward_risk_collection("kolkata", weather)
    assert len(kol["features"]) == 60

    # Test Hyderabad (60 wards)
    hyd = manager.generate_ward_risk_collection("hyderabad", weather)
    assert len(hyd["features"]) == 60

    # Test Lucknow (110 wards)
    lko = manager.generate_ward_risk_collection("lucknow", weather)
    assert len(lko["features"]) == 110

    # Test Amritsar (85 wards)
    asr = manager.generate_ward_risk_collection("amritsar", weather)
    assert len(asr["features"]) == 85

    # Test Ludhiana (95 wards)
    ldh = manager.generate_ward_risk_collection("ludhiana", weather)
    assert len(ldh["features"]) == 95


def test_arbitrary_town_dynamic_synthesis():
    manager = MunicipalWardManager()
    weather = {
        "temp_c": 39.0,
        "relative_humidity_pct": 50.0,
        "wind_speed_10m_m_s": 1.5,
        "solar_radiation_w_m2": 650.0
    }

    # Test arbitrary town with coordinates (Fazilka)
    dyn = manager.generate_ward_risk_collection("fazilka", weather, custom_lat=30.4042, custom_lon=74.0270)
    assert len(dyn["features"]) > 0
    assert dyn["metadata"]["city_name"] != ""
    assert dyn["metadata"]["total_wards"] == len(dyn["features"])

    # Test another arbitrary district / town (e.g. Alwar)
    dyn2 = manager.generate_ward_risk_collection("alwar", weather, custom_lat=27.5530, custom_lon=76.6346)
    assert len(dyn2["features"]) > 0
    assert dyn2["features"][0]["properties"]["demographics"]["area_sqkm"] > 0

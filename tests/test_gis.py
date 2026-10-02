"""
Unit tests for GIS Engine and GeoJSON Spatial Risk Attribution.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.gis.engine import GISEngine
from backend.app.thermal.hazard import calculate_thermal_hazard


def test_gis_ward_risk_geojson_generation():
    """Verify GeoJSON layer creation and attribute enrichment."""
    engine = GISEngine()
    
    geojson_path = "data/sample/ahmedabad_wards.geojson"
    census_path = "data/sample/ahmedabad_census_wards.json"
    
    assert os.path.exists(geojson_path)
    assert os.path.exists(census_path)
    
    hazard = calculate_thermal_hazard(
        temp_c=42.0,
        relative_humidity_pct=35.0,
        wind_speed_10m_m_s=2.0,
        solar_radiation_w_m2=750.0
    )
    
    enriched = engine.generate_ward_risk_geojson(
        geojson_path=geojson_path,
        census_path=census_path,
        hazard_data=hazard,
        consecutive_heat_days=2
    )
    
    assert enriched["type"] == "FeatureCollection"
    features = enriched["features"]
    assert len(features) == 20  # 20 Ahmedabad wards
    
    first_feature = features[0]
    props = first_feature["properties"]
    assert "ward_id" in props
    assert "ward_name" in props
    assert "hazard_score" in props
    assert "hazard_resolution" in props
    assert props["hazard_resolution"] == "city_scale_uniform"
    assert "vulnerability_score" in props
    assert "heat_risk_score" in props
    assert "alert_level" in props
    assert "alert_color" in props
    assert "demographics" in props
    assert "metadata" in enriched
    assert "disclaimer" in enriched["metadata"]
    assert enriched["metadata"]["hazard_resolution"] == "city_scale_uniform"


def test_lcz_prototype_multipliers_config():
    """Verify that LCZ prototype multipliers are externalized and labeled as illustrative."""
    import yaml
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "lcz_prototype_multipliers.yaml")
    assert os.path.exists(config_path)
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    assert cfg["status"] == "illustrative_prototype_constants"
    assert cfg["validation_status"] == "unvalidated_simulation_only"
    assert "lcz_classes" in cfg
    assert len(cfg["lcz_classes"]) >= 8

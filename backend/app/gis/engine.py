"""
SIH26083 Spatial GIS & Ward-Level Risk Attribution Engine.

Performs spatial attribution by joining macro-scale biometeorological hazard fields
with Census 2011 demographic vulnerability across municipal ward GeoJSON polygons.
"""

import json
import os
from typing import Dict, Any, List, Optional
from ..vulnerability.demographic import DemographicVulnerabilityEngine
from ..risk.engine import HeatRiskEngine


class GISEngine:
    """
    Manages spatial datasets, GeoJSON parsing, and thematic choropleth generation
    for municipal wards and zones.
    """

    def __init__(
        self,
        vulnerability_engine: Optional[DemographicVulnerabilityEngine] = None,
        risk_engine: Optional[HeatRiskEngine] = None
    ):
        self.vuln_engine = vulnerability_engine or DemographicVulnerabilityEngine()
        self.risk_engine = risk_engine or HeatRiskEngine()

    def load_geojson(self, geojson_path: str) -> Dict[str, Any]:
        """Load and validate GeoJSON FeatureCollection."""
        if not os.path.exists(geojson_path):
            raise FileNotFoundError(f"GeoJSON file not found at: {geojson_path}")
        with open(geojson_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_census_wards(self, census_path: str) -> List[Dict[str, Any]]:
        """Load Census ward demographics JSON."""
        if not os.path.exists(census_path):
            raise FileNotFoundError(f"Census file not found at: {census_path}")
        with open(census_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_ward_risk_geojson(
        self,
        geojson_path: str,
        census_path: str,
        hazard_data: Dict[str, Any],
        consecutive_heat_days: int = 1
    ) -> Dict[str, Any]:
        """
        Produce an enriched GeoJSON FeatureCollection where each ward polygon contains
        both demographic sensitivity and combined Heat-Health Risk metrics.
        
        Args:
            geojson_path: Path to ward boundaries GeoJSON.
            census_path: Path to Census 2011 demographic data.
            hazard_data: Dictionary output from calculate_thermal_hazard().
            consecutive_heat_days: Duration of extreme heat (1 to 5).
            
        Returns:
            Enriched GeoJSON FeatureCollection dictionary ready for Leaflet.js.
        """
        raw_geojson = self.load_geojson(geojson_path)
        raw_census = self.load_census_wards(census_path)

        # 1. Process demographic vulnerability
        processed_wards = self.vuln_engine.process_city_wards(raw_census)
        ward_map = {w["ward_id"]: w for w in processed_wards}

        # 2. Extract macro hazard score
        hazard_score = hazard_data.get("composite_hazard_score", 50.0)
        metrics = hazard_data.get("metrics", {})

        # 3. Enrich GeoJSON features
        enriched_features = []
        for feature in raw_geojson.get("features", []):
            props = feature.get("properties", {})
            w_id = props.get("ward_id")
            
            ward_info = ward_map.get(w_id, {})
            vuln_score = ward_info.get("vulnerability_score", 50.0)

            # Evaluate composite risk for this specific ward
            risk_calc = self.risk_engine.calculate_risk(
                hazard_score=hazard_score,
                vulnerability_score=vuln_score,
                consecutive_heat_days=consecutive_heat_days
            )

            # Build enriched properties
            enriched_props = {
                **props,
                "hazard_score": hazard_score,
                "vulnerability_score": vuln_score,
                "heat_risk_score": risk_calc["risk_score"],
                "alert_level": risk_calc["alert_level"],
                "alert_label": risk_calc["alert_label"],
                "alert_color": risk_calc["alert_color"],
                "action_summary": risk_calc["action_summary"],
                "utci_val": metrics.get("utci", {}).get("value_c"),
                "utci_category": metrics.get("utci", {}).get("category"),
                "wbgt_val": metrics.get("wbgt", {}).get("value_c"),
                "wbgt_risk": metrics.get("wbgt", {}).get("risk_level"),
                "heat_index_val": metrics.get("heat_index", {}).get("value_c"),
                "demographics": ward_info.get("demographics", {})
            }

            enriched_features.append({
                "type": "Feature",
                "geometry": feature.get("geometry"),
                "properties": enriched_props
            })

        return {
            "type": "FeatureCollection",
            "name": raw_geojson.get("name", "Ward_Risk_Layer"),
            "crs": raw_geojson.get("crs"),
            "features": enriched_features,
            "metadata": {
                "attribution": "SIH26083 Ward-Level Risk Attribution Layer",
                "disclaimer": "Ward-level risk attribution joins regional biometeorological hazard with localized demographic vulnerability. Does not claim micro-scale ward-resolution meteorology.",
                "total_wards": len(enriched_features),
                "consecutive_days": consecutive_heat_days
            }
        }

"""
CLI Script to evaluate ward-level risk attribution and save enriched GeoJSON output.
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.gis.engine import GISEngine
from backend.app.thermal.hazard import calculate_thermal_hazard


def main():
    city = sys.argv[1] if len(sys.argv) > 1 else "ahmedabad"
    day = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    geojson_path = "data/sample/ahmedabad_wards.geojson"
    census_path = "data/sample/ahmedabad_census_wards.json"
    
    # Representative heatwave meteorological forcing
    hazard = calculate_thermal_hazard(temp_c=43.0, relative_humidity_pct=42.0, wind_speed_10m_m_s=1.8, solar_radiation_w_m2=760.0)
    
    gis = GISEngine()
    enriched = gis.generate_ward_risk_geojson(
        geojson_path=geojson_path,
        census_path=census_path,
        hazard_data=hazard,
        consecutive_heat_days=day
    )
    
    out_file = f"data/processed/{city}_ward_risk_day{day}.geojson"
    os.makedirs("data/processed", exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)
        
    print(f"[SUCCESS] Generated enriched spatial risk layer: {out_file} ({len(enriched['features'])} wards)")


if __name__ == "__main__":
    main()

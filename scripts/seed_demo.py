"""
Seed & Initialization Script for SIH26083 Prototype.
Pre-populates data directories, validates sample datasets, and prepares local cache.
"""

import os
import json
import sys

# Ensure root path in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.thermal.hazard import calculate_thermal_hazard
from backend.app.gis.engine import GISEngine


def seed():
    print("================================================================")
    print("SIH26083 - Prototype Seeding & Environment Initialization")
    print("================================================================")

    # 1. Create required runtime directories
    dirs = [
        "data/raw",
        "data/processed",
        "data/sample",
        "data/cache",
        "assets/diagrams",
        "assets/screenshots"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"[OK] Verified directory: {d}")

    # 2. Validate sample GeoJSON and Census PCA files
    ahmedabad_geojson = "data/sample/ahmedabad_wards.geojson"
    ahmedabad_census = "data/sample/ahmedabad_census_wards.json"

    if os.path.exists(ahmedabad_geojson) and os.path.exists(ahmedabad_census):
        with open(ahmedabad_census, "r", encoding="utf-8") as f:
            census_data = json.load(f)
        print(f"[OK] Loaded Census 2011 baseline: {len(census_data)} Ahmedabad wards.")

        with open(ahmedabad_geojson, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        print(f"[OK] Loaded GIS Boundaries: {len(geojson_data.get('features', []))} ward polygons.")
    else:
        print("[WARN] Sample data files missing.")

    # 3. Test Biometeorological Engine
    print("\n--- Testing Biometeorological Engine ---")
    hz = calculate_thermal_hazard(temp_c=42.0, relative_humidity_pct=40.0, wind_speed_10m_m_s=2.0, solar_radiation_w_m2=750.0)
    print(f"Air Temp: 42.0°C -> UTCI: {hz['metrics']['utci']['value_c']}°C ({hz['metrics']['utci']['category']})")
    print(f"Occupational WBGT: {hz['metrics']['wbgt']['value_c']}°C ({hz['metrics']['wbgt']['risk_level']})")
    print(f"Composite Hazard Score: {hz['composite_hazard_score']}/100")

    print("\n[SUCCESS] Environment seeded successfully! Start server with:")
    print("python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000")
    print("================================================================")


if __name__ == "__main__":
    seed()

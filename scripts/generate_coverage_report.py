#!/usr/bin/env python3
"""
scripts/generate_coverage_report.py

Generates an authoritative, factual coverage audit report (docs/COVERAGE.md)
for all urban centers supported in Taapamigo (SIH26083).

Audits:
- City name & state
- Spatial boundary type (Official DataMeet GIS polygon, Illustrative Ward Delimitation, or Synthetic LCZ Unit)
- Feature/Ward count
- Demographic data source & quality status
- Geometry source reference URL
"""

import os
import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.gis.city_data import MUNICIPAL_WARD_PROFILES
from backend.app.gis.ward_directory import DATAMEET_CITY_MAP


def generate_coverage():
    datameet_dir = ROOT_DIR / "data" / "datameet_wards"
    sample_dir = ROOT_DIR / "data" / "sample"
    districts_file = sample_dir / "india_census_districts.json"

    with open(districts_file, "r", encoding="utf-8") as f:
        districts_list = json.load(f)
    district_names = {d["district_name"].lower(): d for d in districts_list}

    manifest_file = datameet_dir / "manifest.json"
    manifest_urls = {}
    if manifest_file.exists():
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest_urls = json.load(f)

    # Collect all cities
    all_city_ids = sorted(list(set(list(MUNICIPAL_WARD_PROFILES.keys()) + list(DATAMEET_CITY_MAP.keys()))))
    
    rows = []
    total_real_polygon_cities = 0
    total_illustrative_cities = 0
    total_lcz_synthetic_cities = 0
    total_wards_verified = 0

    for c_id in all_city_ids:
        prof = MUNICIPAL_WARD_PROFILES.get(c_id, {})
        c_name = prof.get("city_name", c_id.title())
        s_name = prof.get("state_name", "India")
        dist_name = prof.get("district_name", c_name)

        # Check geometry
        geojson_filename = DATAMEET_CITY_MAP.get(c_id)
        datameet_path = datameet_dir / geojson_filename if geojson_filename else None
        sample_path = sample_dir / f"{c_id}_wards.geojson"

        geo_type = "Synthetic LCZ Spatial Units"
        ward_count = prof.get("total_wards", 10)
        source_url = "Stewart & Oke (2012) Urban Density Proportional Allocation"
        data_quality = "estimated"

        if c_id == "ahmedabad" and (sample_path.exists() or (datameet_path and datameet_path.exists())):
            geo_type = "Illustrative Ward Delimitation (20 Wards)"
            ward_count = 20
            source_url = "Internal prototype delimitation (DataMeet upstream provides office points)"
            data_quality = "illustrative_prototype"
            total_illustrative_cities += 1
        elif datameet_path and datameet_path.exists():
            try:
                with open(datameet_path, "r", encoding="utf-8") as gf:
                    gj = json.load(gf)
                    feature_cnt = len(gj.get("features", []))
                    if feature_cnt > 0:
                        geo_type = "Official DataMeet Ward Boundary Polygon"
                        ward_count = feature_cnt
                        matched_manifest = next((url for k, url in manifest_urls.items() if k.lower() == c_id.lower()), "https://github.com/datameet/Municipal_Spatial_Data")
                        source_url = f"[DataMeet]({matched_manifest})"
                        total_real_polygon_cities += 1
            except Exception:
                pass
        
        if geo_type == "Synthetic LCZ Spatial Units":
            total_lcz_synthetic_cities += 1

        total_wards_verified += ward_count

        # Demographic Granularity
        matched_dist = district_names.get(dist_name.lower()) or district_names.get(c_name.lower())
        if c_id == "ahmedabad":
            demo_level = "Ward (Illustrative Sample)"
        elif matched_dist:
            demo_level = f"District Baseline ({matched_dist.get('district_name')})"
        else:
            demo_level = "National Urban Baseline"

        rows.append({
            "city": c_name,
            "state": s_name,
            "wards": ward_count,
            "geo_type": geo_type,
            "demo_level": demo_level,
            "data_quality": data_quality,
            "source": source_url
        })

    # Generate Markdown Output
    md = []
    md.append("# Urban Coverage & Data Provenance Registry — Taapamigo (SIH26083)\n")
    md.append("This document provides a factual, verified inventory of all municipal centers supported in Taapamigo, documenting spatial boundary types, demographic granularity, and data provenance.\n")
    md.append("## Coverage Summary Statistics\n")
    md.append(f"- **Total Documented Urban Centers:** {len(rows)}")
    md.append(f"- **Cities with Official DataMeet Polygons:** {total_real_polygon_cities}")
    md.append(f"- **Cities with Illustrative Prototype Delimitation:** {total_illustrative_cities} (Ahmedabad 20 wards)")
    md.append(f"- **Cities with Synthetic LCZ Spatial Units:** {total_lcz_synthetic_cities}")
    md.append(f"- **Total Spatial Units / Wards:** {total_wards_verified:,}\n")
    md.append("## Detailed Urban Center Coverage Table\n")
    md.append("| Urban Center | State | Wards / Units | Spatial Boundary Type | Demographic Granularity | Data Quality | Geometry Source |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    for r in rows:
        md.append(f"| **{r['city']}** | {r['state']} | {r['wards']} | {r['geo_type']} | {r['demo_level']} | `{r['data_quality']}` | {r['source']} |")

    md.append("\n---\n")
    md.append("## Notes on Data Quality Labels\n")
    md.append("- `official_datameet`: Sourced directly from verified open-license government municipal delimitation shapefiles via DataMeet.")
    md.append("- `illustrative_prototype`: Synthetic/stylized municipal delimitation boundaries or population attributes used for interface and algorithm demonstration.")
    md.append("- `estimated`: Demographic attributes computed using state/district percentage baseline models applied to Census 2011 total populations.\n")

    out_path = ROOT_DIR / "docs" / "COVERAGE.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    print(f"[+] Written coverage report for {len(rows)} cities to: {out_path}")


if __name__ == "__main__":
    generate_coverage()

"""
tests/test_data_provenance.py

Automated pytest verification of data integrity and provenance for demographic datasets.
Fails if any demographic record claims raw Census PCA extraction without genuine extraction,
or fails to flag derived percentages with data_quality: estimated.
"""

import json
from pathlib import Path
from scripts.audit_data_provenance import audit_district_provenance, audit_ahmedabad_wards

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_district_demographic_provenance():
    """Verify that all 46 districts are honestly flagged as estimated with transparent methodology."""
    res = audit_district_provenance()
    assert res == 0, "District demographic dataset failed provenance and honesty audit."


def test_ahmedabad_wards_illustrative_flag():
    """Verify that Ahmedabad sample wards are explicitly flagged as illustrative prototype delimitation."""
    res = audit_ahmedabad_wards()
    assert res == 0, "Ahmedabad ward dataset failed illustrative prototype provenance audit."


def test_no_untruthful_pca_claims_in_json():
    """Ensure no row claims direct raw PCA extraction for age 60+ data (which is not in PCA)."""
    districts_file = ROOT_DIR / "data" / "sample" / "india_census_districts.json"
    with open(districts_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for row in data:
        assert row.get("data_quality") in ("estimated", "census_extracted"), f"Missing valid data_quality in {row.get('district_name')}"
        if row.get("data_quality") == "estimated":
            assert "NOT extracted" in row.get("census_source", "") or "Estimated" in row.get("census_source", "")
            assert "method" in row, f"Missing method description in {row.get('district_name')}"

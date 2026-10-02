#!/usr/bin/env python3
"""
scripts/audit_data_provenance.py

Audit script to verify the provenance and integrity of demographic datasets
in Taapamigo (SIH26083).

Reproduces the integrity check:
Identifies whether district-level elderly and outdoor worker counts were computed
from round percentages (tot_pop * pct / 100) rather than extracted from Census tables.
Verifies that any derived/estimated records are truthfully marked with:
  "data_quality": "estimated"
and that census_source does not falsely claim direct raw Census PCA extraction.
"""

import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "sample" / "india_census_districts.json"
AHMEDABAD_PATH = ROOT_DIR / "data" / "sample" / "ahmedabad_census_wards.json"


def audit_district_provenance(file_path: Path = DATA_PATH) -> int:
    print(f"[*] Auditing demographic provenance for: {file_path}")
    if not file_path.exists():
        print(f"[!] File not found: {file_path}")
        return 1

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_rows = len(data)
    derived_elderly_count = 0
    derived_outdoor_count = 0
    missing_quality_flag = 0
    untruthful_source_claims = 0

    print(f"[*] Scanning {total_rows} district records...\n")
    print(f"{'District':<25} {'Elderly Derived?':<18} {'Outdoor Derived?':<18} {'Quality Flag':<15} {'Status'}")
    print("-" * 90)

    for row in data:
        dist_name = row.get("district_name", "Unknown")
        tot_pop = row.get("tot_pop", 0)
        
        elderly_cnt = row.get("pop_elderly_60plus", 0)
        elderly_pct = row.get("elderly_percentage", 0.0)
        calc_elderly = round(tot_pop * elderly_pct / 100)
        is_elderly_derived = (tot_pop > 0) and (abs(elderly_cnt - calc_elderly) <= 1)

        outdoor_cnt = row.get("workers_outdoor", 0)
        outdoor_pct = row.get("outdoor_worker_percentage", 0.0)
        calc_outdoor = round(tot_pop * outdoor_pct / 100)
        is_outdoor_derived = (tot_pop > 0) and (abs(outdoor_cnt - calc_outdoor) <= 1)

        if is_elderly_derived:
            derived_elderly_count += 1
        if is_outdoor_derived:
            derived_outdoor_count += 1

        quality = row.get("data_quality", "unspecified")
        source = row.get("census_source", "")

        # Check if derived counts are honestly flagged
        is_honest = True
        status_flags = []
        if (is_elderly_derived or is_outdoor_derived) and quality != "estimated":
            missing_quality_flag += 1
            is_honest = False
            status_flags.append("MISSING_QUALITY_FLAG")

        # Census PCA does NOT contain age 60+ data (it is in C-Series C-13/C-14)
        if "Census of India 2011 PCA" in source and quality != "estimated" and "NOT extracted" not in source:
            untruthful_source_claims += 1
            is_honest = False
            status_flags.append("UNTRUTHFUL_PCA_CLAIM")

        status_str = "OK" if is_honest else ", ".join(status_flags)
        print(f"{dist_name:<25} {str(is_elderly_derived):<18} {str(is_outdoor_derived):<18} {quality:<15} {status_str}")

    print("\n" + "=" * 90)
    print(f"Summary:")
    print(f"  Total Districts Analyzed:        {total_rows}")
    print(f"  Derived Elderly Counts:          {derived_elderly_count} / {total_rows} ({derived_elderly_count/total_rows*100:.1f}%)")
    print(f"  Derived Outdoor Worker Counts:   {derived_outdoor_count} / {total_rows} ({derived_outdoor_count/total_rows*100:.1f}%)")
    print(f"  Missing 'estimated' Quality Flag: {missing_quality_flag}")
    print(f"  Untruthful Source Claims:        {untruthful_source_claims}")
    print("=" * 90)

    if missing_quality_flag > 0 or untruthful_source_claims > 0:
        print(f"[FAIL] Data provenance audit failed: {missing_quality_flag + untruthful_source_claims} violations detected.")
        return 1
    
    print("[PASS] All demographic records have honest provenance flags and accurate labels.")
    return 0


def audit_ahmedabad_wards(file_path: Path = AHMEDABAD_PATH) -> int:
    print(f"\n[*] Auditing Ahmedabad ward provenance for: {file_path}")
    if not file_path.exists():
        print(f"[!] File not found: {file_path}")
        return 1

    with open(file_path, "r", encoding="utf-8") as f:
        wards = json.load(f)

    violations = 0
    for w in wards:
        if not w.get("is_illustrative", False):
            violations += 1
        if w.get("data_quality") not in ("illustrative_prototype", "estimated"):
            violations += 1

    if violations > 0:
        print(f"[FAIL] Ahmedabad wards audit failed: {violations} missing illustrative flags.")
        return 1

    print("[PASS] Ahmedabad wards correctly flagged as illustrative prototype delimitation.")
    return 0


if __name__ == "__main__":
    ret1 = audit_district_provenance()
    ret2 = audit_ahmedabad_wards()
    sys.exit(ret1 or ret2)

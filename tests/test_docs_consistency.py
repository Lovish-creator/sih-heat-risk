"""
Test Suite for Documentation and Model Specification Consistency.
Ensures config/risk_weights.yaml, backend/app/core/constants.py, and docs/MODEL_SPEC.md
remain perfectly aligned with identical weights, versions, and thresholds.
"""

import os
import yaml
import pytest
from backend.app.core.constants import (
    MODEL_VERSION,
    HAZARD_WEIGHT,
    VULNERABILITY_WEIGHT,
    DURATION_WEIGHT,
    HAZARD_SUBWEIGHT_UTCI,
    HAZARD_SUBWEIGHT_WBGT,
    HAZARD_SUBWEIGHT_HEAT_INDEX,
    VULN_SUBWEIGHT_ELDERLY,
    VULN_SUBWEIGHT_OUTDOOR_WORKER,
    VULN_SUBWEIGHT_DENSITY,
    DURATION_SCALING,
    ALERT_THRESHOLD_GREEN_MAX,
    ALERT_THRESHOLD_YELLOW_MAX,
    ALERT_THRESHOLD_ORANGE_MAX,
)


def _get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def test_core_constants_sums():
    """Verify top-level and subcomponent weights sum to exactly 1.0."""
    top_sum = HAZARD_WEIGHT + VULNERABILITY_WEIGHT + DURATION_WEIGHT
    assert pytest.approx(top_sum, 1e-6) == 1.0

    hazard_sub_sum = HAZARD_SUBWEIGHT_UTCI + HAZARD_SUBWEIGHT_WBGT + HAZARD_SUBWEIGHT_HEAT_INDEX
    assert pytest.approx(hazard_sub_sum, 1e-6) == 1.0

    vuln_sub_sum = VULN_SUBWEIGHT_ELDERLY + VULN_SUBWEIGHT_OUTDOOR_WORKER + VULN_SUBWEIGHT_DENSITY
    assert pytest.approx(vuln_sub_sum, 1e-6) == 1.0


def test_yaml_config_matches_constants():
    """Verify config/risk_weights.yaml matches core/constants.py."""
    root = _get_project_root()
    yaml_path = os.path.join(root, "config", "risk_weights.yaml")
    assert os.path.exists(yaml_path), "risk_weights.yaml must exist"

    with open(yaml_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    assert cfg["model_version"] == MODEL_VERSION
    weights = cfg["weights"]

    # Top-level weights
    assert pytest.approx(weights["thermal_hazard"]["weight"]) == HAZARD_WEIGHT
    assert pytest.approx(weights["demographic_vulnerability"]["weight"]) == VULNERABILITY_WEIGHT
    assert pytest.approx(weights["heatwave_duration"]["weight"]) == DURATION_WEIGHT

    # Hazard subweights
    h_sub = weights["thermal_hazard"]["subcomponents"]
    assert pytest.approx(h_sub["utci"]) == HAZARD_SUBWEIGHT_UTCI
    assert pytest.approx(h_sub["wbgt"]) == HAZARD_SUBWEIGHT_WBGT
    assert pytest.approx(h_sub["heat_index"]) == HAZARD_SUBWEIGHT_HEAT_INDEX

    # Vulnerability subweights
    v_sub = weights["demographic_vulnerability"]["subcomponents"]
    assert pytest.approx(v_sub["elderly_population_ratio"]) == VULN_SUBWEIGHT_ELDERLY
    assert pytest.approx(v_sub["outdoor_worker_ratio"]) == VULN_SUBWEIGHT_OUTDOOR_WORKER
    assert pytest.approx(v_sub["population_density_norm"]) == VULN_SUBWEIGHT_DENSITY

    # Duration scaling steps
    d_scale = weights["heatwave_duration"]["consecutive_days_scaling"]
    assert pytest.approx(d_scale["day_1"]) == DURATION_SCALING[1]
    assert pytest.approx(d_scale["day_2"]) == DURATION_SCALING[2]
    assert pytest.approx(d_scale["day_3"]) == DURATION_SCALING[3]
    assert pytest.approx(d_scale["day_4_plus"]) == DURATION_SCALING[4]


def test_model_spec_markdown_matches_constants():
    """Verify docs/MODEL_SPEC.md contains the exact canonical constants and thresholds."""
    root = _get_project_root()
    spec_path = os.path.join(root, "docs", "MODEL_SPEC.md")
    assert os.path.exists(spec_path), "MODEL_SPEC.md must exist"

    with open(spec_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Model version
    assert MODEL_VERSION in content

    # Component weights
    assert f"`{HAZARD_WEIGHT:.2f}`" in content
    assert f"`{VULNERABILITY_WEIGHT:.2f}`" in content
    assert f"`{DURATION_WEIGHT:.2f}`" in content

    # Subweights
    assert f"`{HAZARD_SUBWEIGHT_UTCI:.2f}`" in content
    assert f"`{HAZARD_SUBWEIGHT_WBGT:.2f}`" in content
    assert f"`{HAZARD_SUBWEIGHT_HEAT_INDEX:.2f}`" in content
    assert f"`{VULN_SUBWEIGHT_ELDERLY:.2f}`" in content
    assert f"`{VULN_SUBWEIGHT_OUTDOOR_WORKER:.2f}`" in content
    assert f"`{VULN_SUBWEIGHT_DENSITY:.2f}`" in content

    # Duration values
    assert "`0.00`" in content
    assert "`0.33`" in content
    assert "`0.66`" in content
    assert "`1.00`" in content

    # Day-1 max risk quirk
    assert "85.0" in content

    # Alert thresholds
    assert f"{ALERT_THRESHOLD_GREEN_MAX:.1f}" in content
    assert f"{ALERT_THRESHOLD_YELLOW_MAX:.1f}" in content
    assert f"{ALERT_THRESHOLD_ORANGE_MAX:.1f}" in content

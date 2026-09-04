"""
Unit tests for Wet Bulb Globe Temperature (WBGT) and Stull psychrometric wet-bulb formulation.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.thermal.wbgt import (
    calculate_wet_bulb_stull,
    calculate_globe_temp,
    calculate_wbgt,
    classify_wbgt
)


def test_stull_wet_bulb():
    """Verify Stull psychrometric wet bulb formula against known psychrometric points."""
    # At 20 C, 50% RH: Tw is approx 13.7 C
    tw = calculate_wet_bulb_stull(20.0, 50.0)
    assert 13.0 <= tw <= 14.5

    # At 100% RH: Tw must equal Ta
    tw_100 = calculate_wet_bulb_stull(30.0, 100.0)
    assert abs(tw_100 - 30.0) < 0.8

    # At 35 C, 40% RH: Tw is approx 23.5 C
    tw_hot = calculate_wet_bulb_stull(35.0, 40.0)
    assert 22.0 <= tw_hot <= 25.0


def test_wbgt_outdoor_vs_shade():
    """Outdoor WBGT with strong solar irradiance should exceed shade WBGT."""
    ta = 38.0
    rh = 55.0
    ws = 1.2
    solar = 800.0
    
    wbgt_sun = calculate_wbgt(ta, rh, ws, solar, is_outdoor=True)
    wbgt_shade = calculate_wbgt(ta, rh, ws, solar, is_outdoor=False)
    
    assert wbgt_sun > wbgt_shade
    assert wbgt_sun >= 32.0  # Extreme risk under intense sun + high RH


def test_wbgt_niosh_classification():
    """Verify NIOSH risk classification and rest work regimen assignment."""
    # Low risk
    low = classify_wbgt(26.0)
    assert low["risk_level"] == "Low Risk"
    assert low["hazard_score"] <= 25.0

    # Extreme risk
    extreme = classify_wbgt(33.5)
    assert extreme["risk_level"] == "Extreme Risk"
    assert "Halt Heavy Outdoor Labor" in extreme["work_rest_regimen"] or "25% Work" in extreme["work_rest_regimen"]
    assert extreme["hazard_score"] == 100.0

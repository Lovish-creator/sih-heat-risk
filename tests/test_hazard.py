"""
Unit tests for Composite Thermal Hazard Engine.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.thermal.hazard import calculate_thermal_hazard


def test_thermal_hazard_contrast_demo():
    """
    CRITICAL DEMO TEST:
    Compare two environmental scenarios with the exact same air temperature (40 C)
    Scenario A: 40 C, 15% RH, 5.0 m/s wind, 150 W/m^2 solar (Dry, windy, hazy/shade)
    Scenario B: 40 C, 70% RH, 0.8 m/s wind, 800 W/m^2 solar (Humid, stagnant, intense sun)
    """
    hazard_a = calculate_thermal_hazard(
        temp_c=40.0,
        relative_humidity_pct=15.0,
        wind_speed_10m_m_s=5.0,
        solar_radiation_w_m2=150.0
    )
    
    hazard_b = calculate_thermal_hazard(
        temp_c=40.0,
        relative_humidity_pct=70.0,
        wind_speed_10m_m_s=0.8,
        solar_radiation_w_m2=800.0
    )
    
    # Assert Scenario B produces drastically higher hazard despite identical 40 C air temp
    assert hazard_b["composite_hazard_score"] > hazard_a["composite_hazard_score"] + 30.0
    assert hazard_b["metrics"]["utci"]["value_c"] > hazard_a["metrics"]["utci"]["value_c"] + 10.0
    assert hazard_b["metrics"]["wbgt"]["value_c"] > hazard_a["metrics"]["wbgt"]["value_c"] + 5.0


def test_thermal_hazard_bounds():
    """Assert composite hazard score is strictly bounded between 0 and 100."""
    # Freezing case
    h_cold = calculate_thermal_hazard(0.0, 50.0, 2.0, 0.0)
    assert 0.0 <= h_cold["composite_hazard_score"] <= 100.0

    # Extreme heat case
    h_extreme = calculate_thermal_hazard(48.0, 80.0, 0.5, 900.0)
    assert 0.0 <= h_extreme["composite_hazard_score"] <= 100.0
    assert h_extreme["composite_hazard_score"] >= 95.0

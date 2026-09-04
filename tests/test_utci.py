"""
Unit tests for UTCI (Universal Thermal Climate Index) Calculation.
Validates Bröde et al. (2012) polynomial implementation against reference bounds.
"""

import pytest
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.thermal.utci import (
    calculate_utci,
    classify_utci,
    calculate_vapor_pressure,
    calculate_mrt
)


def test_vapor_pressure_magnus():
    """Test Magnus-Tetens vapor pressure calculation at known points."""
    # At 20 C and 50% RH: saturation pressure es ~ 23.38 hPa -> e ~ 11.69 hPa
    e = calculate_vapor_pressure(20.0, 50.0)
    assert 11.0 <= e <= 12.5

    # At 40 C and 50% RH: saturation pressure es ~ 73.7 hPa -> e clamped to 50 hPa
    e_hot = calculate_vapor_pressure(40.0, 50.0)
    assert 35.0 <= e_hot <= 50.0

    # At 0% RH
    e_zero = calculate_vapor_pressure(30.0, 0.0)
    assert e_zero == 0.0


def test_mrt_stefan_boltzmann():
    """Test Mean Radiant Temperature calculation."""
    # Zero solar radiation -> Tmrt equals air temperature
    tmrt_night = calculate_mrt(35.0, 0.0)
    assert abs(tmrt_night - 35.0) < 0.1

    # High solar radiation 800 W/m^2 -> Tmrt elevated above air temperature
    tmrt_sun = calculate_mrt(35.0, 800.0)
    assert tmrt_sun > 35.0
    assert tmrt_sun - 35.0 <= 30.0


def test_utci_reference_cases():
    """Test UTCI calculations under contrasting meteorological conditions."""
    # 1. Comfortable conditions: 20 C, 50% RH, 1.0 m/s wind, 0 solar
    utci_comfort = calculate_utci(20.0, 50.0, 1.0, 0.0)
    assert 18.0 <= utci_comfort <= 23.0
    info = classify_utci(utci_comfort)
    assert info["code"] == "NO_THERMAL_STRESS"

    # 2. Hot, humid, sunny conditions (Severe heat stress): 40 C, 65% RH, 0.8 m/s, 700 W/m^2
    utci_extreme = calculate_utci(40.0, 65.0, 0.8, 700.0)
    assert utci_extreme >= 46.0
    info_extreme = classify_utci(utci_extreme)
    assert info_extreme["code"] == "EXTREME_HEAT_STRESS"
    assert info_extreme["hazard_score"] == 100.0

    # 3. Hot, dry, windy conditions (Lower heat stress at same Ta=40 C): 40 C, 15% RH, 5.0 m/s, 100 W/m^2
    utci_dry_wind = calculate_utci(40.0, 15.0, 5.0, 100.0)
    assert utci_dry_wind < utci_extreme
    assert utci_dry_wind <= 38.0


def test_utci_monotonicity_with_humidity():
    """Assert UTCI increases monotonically with relative humidity at fixed high temperature."""
    ta = 38.0
    v10 = 1.5
    rad = 400.0
    
    utci_low_rh = calculate_utci(ta, 20.0, v10, rad)
    utci_med_rh = calculate_utci(ta, 50.0, v10, rad)
    utci_high_rh = calculate_utci(ta, 80.0, v10, rad)
    
    assert utci_low_rh < utci_med_rh < utci_high_rh

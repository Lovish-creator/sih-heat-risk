"""
Unit tests for NOAA/NWS Rothfusz Heat Index calculation.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.thermal.heat_index import calculate_heat_index, classify_heat_index


def test_heat_index_rothfusz():
    """Verify Heat Index values at NOAA reference points."""
    # At 32 C (90 F) and 60% RH: Heat Index is ~38 C (~100 F)
    hi_32 = calculate_heat_index(32.2, 60.0)
    assert 36.0 <= hi_32 <= 40.0

    # At 40 C (104 F) and 60% RH: Dangerous apparent temperature (>55 C)
    hi_extreme = calculate_heat_index(40.0, 60.0)
    assert hi_extreme >= 52.0
    info = classify_heat_index(hi_extreme)
    assert info["code"] in ["DANGER", "EXTREME_DANGER"]

    # At low temperature (20 C): Heat Index equals or is near ambient
    hi_cool = calculate_heat_index(20.0, 50.0)
    assert abs(hi_cool - 20.0) < 2.0


def test_heat_index_monotonicity():
    """Higher RH at fixed hot temp should strictly increase Heat Index."""
    hi_20 = calculate_heat_index(35.0, 20.0)
    hi_50 = calculate_heat_index(35.0, 50.0)
    hi_80 = calculate_heat_index(35.0, 80.0)
    
    assert hi_20 < hi_50 < hi_80

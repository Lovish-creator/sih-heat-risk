"""
Unit tests for Public Health & Occupational Advisory Engine.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.advisory.engine import AdvisoryEngine


def test_advisory_generation_for_all_personas():
    """Verify that advisories contain distinct actionable content for all 3 target personas."""
    engine = AdvisoryEngine()
    
    wbgt_mock = {"work_rest_regimen": "25% Work / 75% Rest per hour"}
    utci_mock = {"category": "Extreme Heat Stress"}
    
    adv_red = engine.generate_advisories("RED", 88.0, wbgt_mock, utci_mock)
    
    personas = adv_red["personas"]
    assert "general_public" in personas
    assert "outdoor_workers" in personas
    assert "authorities" in personas
    
    # Assert specific actions
    assert any("Avoid all non-essential outdoor exposure" in act for act in personas["general_public"]["actions"])
    assert any("OCCUPATIONAL DIRECTIVE" in act for act in personas["outdoor_workers"]["actions"])
    assert any("Level-3 Red Emergency" in act for act in personas["authorities"]["actions"])
    assert "provenance" in adv_red

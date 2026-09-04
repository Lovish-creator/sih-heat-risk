"""
Unit tests for Heat-Health Risk Engine.
Validates monotonicity, duration escalation, and IMD 4-tier alert assignment.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.risk.engine import HeatRiskEngine


def test_risk_monotonicity():
    """
    CRITICAL RISK PROPERTY:
    Risk must be strictly monotonic with respect to hazard, vulnerability, and duration.
    """
    engine = HeatRiskEngine()
    
    # 1. Higher hazard -> Higher risk
    risk_low_hazard = engine.calculate_risk(hazard_score=30.0, vulnerability_score=50.0, consecutive_heat_days=1)
    risk_high_hazard = engine.calculate_risk(hazard_score=80.0, vulnerability_score=50.0, consecutive_heat_days=1)
    assert risk_high_hazard["risk_score"] > risk_low_hazard["risk_score"]
    
    # 2. Higher vulnerability -> Higher risk
    risk_low_vuln = engine.calculate_risk(hazard_score=60.0, vulnerability_score=20.0, consecutive_heat_days=1)
    risk_high_vuln = engine.calculate_risk(hazard_score=60.0, vulnerability_score=80.0, consecutive_heat_days=1)
    assert risk_high_vuln["risk_score"] > risk_low_vuln["risk_score"]
    
    # 3. Consecutive heat days duration -> Higher risk
    risk_day1 = engine.calculate_risk(hazard_score=70.0, vulnerability_score=60.0, consecutive_heat_days=1)
    risk_day4 = engine.calculate_risk(hazard_score=70.0, vulnerability_score=60.0, consecutive_heat_days=4)
    assert risk_day4["risk_score"] > risk_day1["risk_score"]


def test_alert_level_classification():
    """Test 4-tier alert level classification (Green, Yellow, Orange, Red)."""
    engine = HeatRiskEngine()
    
    res_green = engine.calculate_risk(10.0, 10.0, 1)
    assert res_green["alert_level"] == "GREEN"
    
    res_yellow = engine.calculate_risk(45.0, 40.0, 1)
    assert res_yellow["alert_level"] == "YELLOW"
    
    res_orange = engine.calculate_risk(75.0, 60.0, 1)
    assert res_orange["alert_level"] == "ORANGE"
    
    res_red = engine.calculate_risk(95.0, 90.0, 4)
    assert res_red["alert_level"] == "RED"
    assert "disclaimer" in res_red

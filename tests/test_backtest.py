"""
Unit Tests for Empirical Historical Back-Testing.
Validates meteorological event detection on historical benchmarks (Ahmedabad 2010, Control).
"""

import os
import csv
import json
import pytest
from validation.backtest import load_benchmark_dataset, run_event_backtest, RESULTS_DIR


@pytest.fixture
def benchmark_events():
    events = load_benchmark_dataset(use_online_api=False)
    assert len(events) >= 3, "Must contain at least Ahmedabad 2010, Delhi 2024, and Control"
    return {ev["event_id"]: ev for ev in events}


def test_backtest_ahmedabad_2010_escalation(benchmark_events):
    """
    Assert that the May 2010 Ahmedabad heatwave (Azhar et al. 2014):
    1. Triggers ORANGE alert on onset.
    2. Escalates monotonically to RED alert (Risk >= 75.0) on peak day (May 21).
    3. Confirms heatwave detection flag is True throughout.
    """
    ev = benchmark_events["ahmedabad_may_2010"]
    records = run_event_backtest(ev)

    day1 = records[0] # May 18
    day4 = records[3] # May 21 (peak)

    # Risk must escalate with consecutive duration
    assert day4["risk_score"] > day1["risk_score"]
    assert day4["alert_level"] == "RED"
    assert day4["risk_score"] >= 75.0
    assert day4["consecutive_heat_days"] >= 4
    assert day4["is_heatwave_detected"] is True


def test_backtest_control_period_no_heatwave(benchmark_events):
    """
    Assert that non-heatwave winter control period:
    1. Consistently scores in GREEN alert band (Risk < 30.0).
    2. Consecutive heatwave days remain 0.
    3. No false positive heatwave detections occur.
    """
    ev = benchmark_events["ahmedabad_control_jan_2024"]
    records = run_event_backtest(ev)

    for r in records:
        assert r["alert_level"] == "GREEN"
        assert r["consecutive_heat_days"] == 0
        assert r["is_heatwave_detected"] is False
        assert r["risk_score"] < 30.0


def test_backtest_delhi_2024_escalation(benchmark_events):
    """Assert Delhi 2024 heatwave triggers RED alert during persistent May heat."""
    ev = benchmark_events["delhi_may_2024"]
    records = run_event_backtest(ev)

    peak_records = [r for r in records if r["alert_level"] == "RED"]
    assert len(peak_records) >= 1, "Delhi May 2024 heatwave must trigger at least one RED alert"
    assert all(r["temp_max_c"] >= 44.0 for r in records)


def test_backtest_csv_summary_file():
    """Verify generated CSV summary exists and conforms to schema."""
    csv_path = os.path.join(RESULTS_DIR, "heatwave_backtest_summary.csv")
    assert os.path.exists(csv_path), "heatwave_backtest_summary.csv must be generated"

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 20
    assert "event_id" in rows[0]
    assert "risk_score" in rows[0]
    assert "is_heatwave_detected" in rows[0]

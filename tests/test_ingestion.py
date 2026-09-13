"""
Unit Tests for Ingestion Scheduler and ML extension scaffolding.
"""

import pytest
import pandas as pd
from backend.app.risk.engine import HeatRiskEngine
from ml.datasets import HealthOutcomeDataset
from ml.model_registry import ModelRegistry


def test_risk_weights_validation():
    engine = HeatRiskEngine()
    assert abs(sum(engine.weights.values()) - 1.0) < 1e-5

    # Should raise error if weights do not sum to 1.0
    engine.weights["thermal_hazard"] = 0.90
    with pytest.raises(ValueError):
        engine._validate_weights()


def test_ml_dataset_truthfulness_guard():
    # Attempting to train without health labels must raise ValueError
    df_no_labels = pd.DataFrame({
        "record_date": ["2026-06-01", "2026-06-02"],
        "temp_c": [41.0, 42.0],
        "relative_humidity_pct": [35.0, 30.0],
        "utci_c": [45.0, 46.0]
    })
    dataset = HealthOutcomeDataset(df_no_labels)
    with pytest.raises(ValueError, match="No genuine health outcome target labels"):
        dataset.validate_for_training()


def test_model_registry_active_baseline():
    registry = ModelRegistry()
    active = registry.get_active_model_info()
    assert active["is_active"] is True
    assert "baseline" in active["version"]

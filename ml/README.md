# Machine Learning Subsystem & Future Research Scaffolding

## Purpose & Scope

The `ml/` package provides architectural scaffolding and interface contracts for future epidemiological model calibration and empirical health outcome regression.

> **Tier-1 Prototype Policy:**
> "The current Tier-1 prototype does not train or deploy a mortality prediction model. Machine-learning development is reserved for a later stage when legitimate historical health outcomes, sufficient sample size, governance approval, and independent validation are available."

---

## Architectural Rules

1. **Zero Synthetic Mortality / Morbidity Labels:**
   The `HealthOutcomeDataset` explicitly enforces validation (`validate_for_training()`) that rejects training attempts if genuine health registry records (`heat_related_cases`, `hospital_admissions`, `mortality_count`) are absent.
   Training ML models on deterministic mathematical risk scores and calling them "AI mortality predictions" is strictly prohibited.

2. **Active Baseline:**
   The production default model managed by `ModelRegistry` is `deterministic_baseline` (`baseline-0.2`), which implements peer-reviewed deterministic biometeorology (UTCI COST 730, NIOSH WBGT, NOAA Heat Index) combined with Census 2011 PCA demographic vulnerability indicators.

3. **Future Tier-2 / Tier-3 Workflow:**
   When statutory access to verified municipal health surveillance (e.g. IHIP syndromic feeds, Civil Registration System death registries) is secured:
   ```
   Historical Weather & Reanalysis
   + Biometeorological Indices (UTCI, WBGT)
   + Census Vulnerability Indicators
   → Genuine Aggregated Health Outcomes (IDSP / HMIS / CRS)
   → Feature Engineering (ml/feature_engineering.py)
   → Train / Validation / Test Temporal Split
   → Distributed Lag Non-linear Model (DLNM) / GBDT Training (ml/training.py)
   → Empirical Calibration & Uncertainty Estimation
   → Independent Scientific Validation (ml/evaluation.py)
   → Controlled Institutional Deployment via Model Registry (ml/model_registry.py)
   ```

---

## Module Overview

| Module | Status | Purpose |
|---|---|---|
| `ml/datasets.py` | Scaffolding | Structured dataset container with non-negotiable truthfulness validation guard |
| `ml/feature_engineering.py` | Scaffolding | Lagged meteorological features and rolling heat accumulation transformation |
| `ml/training.py` | Scaffolding | Model training pipeline extension point (executes only with valid labels) |
| `ml/evaluation.py` | Scaffolding | Statistical metrics (RMSE, MAE, R², Brier Score, calibration curves) |
| `ml/inference.py` | Scaffolding | Batch and real-time inference wrapper with deterministic fallback |
| `ml/model_registry.py` | Implemented | Versioned model catalog tracking baseline and experimental model metadata |

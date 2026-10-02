# Empirical Back-Testing & Validation Engine — Taapamigo

This directory contains the automated back-testing pipeline used to empirically evaluate the Taapamigo Biometeorological & Heat-Health Risk Engine against historical benchmark heatwaves in India.

---

> [!IMPORTANT]
> ### SCIENTIFIC & VALIDATION DISCLAIMER
> **This validates meteorological event detection only. It does not validate mortality or morbidity prediction, and the weights remain uncalibrated.**
>
> The composite risk index computed by Taapamigo ($0.55\cdot H + 0.30\cdot V + 0.15\cdot D$) is an interpretable multi-criteria spatial prioritization model designed for municipal emergency resource dispatch. It is **not** an epidemiologically fitted statistical mortality prediction model.

---

## 1. Quick Start

Run the complete backtest and regenerate all validation summaries and charts:

```bash
# Execute offline validation using cached ERA5 reanalysis benchmarks
python validation/backtest.py
```

To run automated regression tests:
```bash
python -m pytest tests/test_backtest.py -v
```

---

## 2. Directory Structure

```
validation/
├── backtest.py                         # Master back-testing script
├── README.md                           # This document
└── results/                            # Generated validation artifacts
    ├── heatwave_backtest_summary.csv   # Day-by-day tabular results for 20 benchmark days
    └── backtest_detection_timeline.png # Multi-panel visualization plot
```

---

## 3. Benchmark Scenarios

1. **Ahmedabad Super Heatwave (May 18–24, 2010):**
   - Literature Reference: **Azhar et al. (2014)**, *PLOS ONE* (1,344 excess deaths, peak $46.8^\circ\text{C}$).
   - Validates that consecutive heat escalation transitions from ORANGE on onset to **RED Alert ($79.6/100$)** on peak day May 21.

2. **Delhi Severe Heatwave (May 25–31, 2024):**
   - High-temperature multi-day heatwave ($T_{\max} \ge 44.4^\circ\text{C}$ throughout).
   - Validates multi-day duration scaling reaching **RED Alert ($79.1/100$)** on May 28–29.

3. **Ahmedabad Winter Control Period (January 15–20, 2024):**
   - Non-heatwave control baseline ($T_{\max} \approx 26.5–27.7^\circ\text{C}$).
   - Validates zero false alarms: risk remains within **GREEN Alert ($23.2–25.3/100$)** with zero consecutive days.

---

## 4. Comprehensive Documentation

For the full methodology, quantitative tables, and physiological analysis, refer to:
- [`docs/VALIDATION.md`](../docs/VALIDATION.md) — Complete Empirical Validation Report
- [`docs/MODEL_SPEC.md`](../docs/MODEL_SPEC.md) — Authoritative Model Specification

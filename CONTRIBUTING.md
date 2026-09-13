# Contributing to ThermoShield India (SIH26083)

Thank you for contributing to ThermoShield India! This project is engineered as an open, scientifically rigorous, and reproducible early warning system for extreme heatwaves and human thermal stress across Indian municipal corporations.

---

## 1. Development Philosophy

1. **Scientific Correctness First:** Biometeorological indices (UTCI, WBGT, Heat Index) must strictly follow peer-reviewed formulations (COST 730, ISO 7243, Rothfusz). Never alter physical constants or equations without citing literature.
2. **Transparent Data Provenance:** Never fabricate synthetic health or mortality data. Always flag synthetic or generated geometries explicitly.
3. **Modular Simplicity:** Maintain the modular monolith design. Avoid unnecessary distributed dependencies unless justified by measurable scaling requirements.

---

## 2. Setting Up Local Environment

### 2.1 Clone and Install
```bash
# Clone the repository
git clone https://github.com/Lovish-creator/sih-heat-risk.git
cd sih-heat-risk

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Initialize Local Database
```bash
python scripts/seed_db.py
```

### 2.3 Run Local Server
```bash
python run_local.py
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) for the UI and [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

---

## 3. Code Standards & Style Guide

* **Python Version:** 3.10+ compatible.
* **Formatting:** PEP 8 compliance.
* **Type Annotations:** Full type hints on all public functions, classes, and methods.
* **Data Validation:** Use Pydantic models for all API request/response schemas.
* **Database Access:** Encapsulate all database queries inside SQLAlchemy repository classes (`backend/app/db/repositories/`).

---

## 4. Testing Requirements

All contributions must pass the automated test suite without warnings:

```bash
# Run all tests
python -m pytest

# Run with verbose output and coverage
python -m pytest -v --tb=short
```

When adding new biometeorological algorithms, vulnerability indicators, or API routes, include corresponding unit and integration tests in `tests/`.

---

## 5. Submitting Pull Requests

1. Fork the repository and create a feature branch (`git checkout -b feature/your-feature-name`).
2. Implement your changes following the architectural and provenance guidelines.
3. Verify that all 50+ automated tests pass (`python -m pytest`).
4. Commit your changes with clear, descriptive commit messages.
5. Push to your branch and submit a Pull Request to `main`.

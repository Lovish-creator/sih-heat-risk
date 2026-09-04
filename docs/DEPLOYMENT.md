# SIH26083 Deployment & Operations Guide

This guide details instructions for setting up, running, testing, and containerizing the SIH26083 Human Thermal Stress and Early Warning prototype on any clean machine.

---

## 1. System Requirements
- **Python**: 3.10, 3.11, 3.12, 3.13, or 3.14
- **Operating System**: Linux / macOS / Windows 10/11
- **Optional**: Docker 24.0+ & Docker Compose v2+

---

## 2. Local Setup (Standard Python Environment)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/sih26083-heat-risk.git
cd sih26083-heat-risk
```

### Step 2: Create and Activate a Virtual Environment
```bash
# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Linux / macOS (Bash)
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
# Copy example configuration
cp .env.example .env
```

### Step 5: Seed Demo Data & GIS Boundaries
```bash
python scripts/seed_demo.py
```

### Step 6: Start the FastAPI Backend Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Open Web Dashboard: `http://localhost:8000/`
- Interactive OpenAPI Docs (Swagger UI): `http://localhost:8000/docs`

---

## 3. Containerized Deployment (Docker & Docker Compose)

### Single Command Docker Startup
```bash
docker-compose up --build -d
```
Verify container status:
```bash
docker ps
```
Access dashboard at `http://localhost:8000/`.

---

## 4. Running the Verification & Test Suite
```bash
# Run complete pytest test suite
pytest -v tests/

# Run comparative biometeorological scenario demo script
python scripts/compare_scenarios.py
```

# Deployment & Operations Guide — ThermoShield India (SIH26083)

This guide details instructions for launching, configuring, containerizing, and deploying ThermoShield India across local environments, Docker, and production cloud infrastructure.

---

## 1. Quick Start: Local Zero-Configuration Launch

ThermoShield India includes an automated SQLite bootstrap requiring zero database setup.

### 1.1 Prerequisites
* Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.13, 3.14)
* pip / virtualenv

### 1.2 Windows Launch
Double-click `scripts/run_local.bat` or run via PowerShell:
```powershell
.\scripts\run_local.ps1
```
Or directly using Python:
```bash
python run_local.py
```

### 1.3 Linux / macOS Launch
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_local.py
```

### 1.4 Access URLs
* **Interactive Web Dashboard:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Swagger UI / Interactive API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc API Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **System Health Check:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 2. Environment Configuration (`.env`)

Copy `.env.example` to `.env` to customize settings:

```ini
# Core Application Settings
APP_ENV=development                    # development | staging | production
DEBUG=false
DATA_MODE=hybrid                       # live | static | hybrid
ENABLE_FALLBACK_DATA=true              # Set false in production for strict live failover

# Database Connection
# Zero-config SQLite (default):
DATABASE_URL=sqlite:///./data/heat_risk.db
# Or Production PostgreSQL with PostGIS:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/heat_risk

# Server Binding
HOST=127.0.0.1
PORT=8000
WORKERS=1

# Ingestion Scheduling
INGESTION_INTERVAL_MINUTES=15
```

---

## 3. Containerized Deployment (Docker & Docker Compose)

ThermoShield includes production-ready multi-stage Docker configurations.

### 3.1 Launch with Docker Compose (SQLite Standalone)
```bash
docker-compose up --build
```

### 3.2 Launch with PostgreSQL + PostGIS Backend
Update `docker-compose.yml` to uncomment the postgres service, then run:
```bash
docker-compose --profile postgres up --build
```

### 3.3 Container Health Check
The Docker container automatically verifies service availability via:
```bash
curl -f http://localhost:8000/health || exit 1
```

---

## 4. Production Cloud Deployment

### 4.1 Production Server Setup (Ubuntu / Debian Linux)
```bash
# 1. System packages
sudo apt update && sudo apt install -y python3-pip python3-venv git nginx

# 2. Clone repository
git clone https://github.com/Lovish-creator/sih-heat-risk.git /opt/thermoshield
cd /opt/thermoshield

# 3. Virtualenv & Dependencies
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Initialize Database
python scripts/seed_db.py

# 5. Systemd Service Setup (/etc/systemd/system/thermoshield.service)
sudo cp deployment/thermoshield.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now thermoshield
```

### 4.2 Nginx Reverse Proxy Configuration
```nginx
server {
    listen 80;
    server_name thermoshield.example.gov.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 5. Automated Verification & Testing

Before deploying updates to staging or production, run the test suite:

```bash
# Run all 50 automated tests
python -m pytest

# Run with verbose output and duration analysis
python -m pytest -v --durations=10
```

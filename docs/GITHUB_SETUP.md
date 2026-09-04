# SIH26083 GitHub Repository Setup & Push Guide

This document provides exact Git commands for maintaining clean version control, branch hygiene, and publishing to GitHub.

---

## 1. Local Git Initialization
If not already initialized, execute from the repository root:

```bash
git init -b main
git config user.name "SIH26083 Team"
git config user.email "team@sih26083.internal"
```

---

## 2. Structured Commit Sequence

We adhere to the Conventional Commits specification:

```bash
# 1. Initialize project structure and baseline configuration
git add .gitignore .env.example requirements.txt pyproject.toml Dockerfile docker-compose.yml config/
git commit -m "chore: initialize sih26083 project structure and configuration"

# 2. Add authoritative source registry and research reviews
git add data/SOURCE_REGISTRY.md data/data_dictionary.md docs/
git commit -m "docs: add problem interpretation, source registry, and research review"

# 3. Add biometeorological science engines and tests
git add backend/app/thermal/ tests/test_utci.py tests/test_wbgt.py tests/test_heat_index.py
git commit -m "feat(science): implement validated UTCI, WBGT, and Heat Index thermal engines"

# 4. Add demographic vulnerability, risk engine, and advisories
git add backend/app/vulnerability/ backend/app/risk/ backend/app/advisory/ tests/
git commit -m "feat(risk): implement Census demographic vulnerability and NCDC advisory engines"

# 5. Add spatial GIS engine and GeoJSON data
git add backend/app/gis/ data/sample/
git commit -m "feat(gis): add ward-level risk attribution engine and GeoJSON layers"

# 6. Add data providers, cache, and FastAPI backend
git add backend/app/data_sources/ backend/app/api/ backend/app/main.py
git commit -m "feat(backend): implement NASA POWER ingestion adapter and FastAPI REST API"

# 7. Add interactive frontend dashboard
git add frontend/
git commit -m "feat(frontend): build interactive Leaflet and Chart.js heat risk dashboard"

# 8. Add demo scripts, verification notebooks, and final documentation
git add scripts/ notebooks/ README.md FINAL_BUILD_REPORT.md
git commit -m "feat(demo): add comparative biometeorological scenarios and final documentation"
```

---

## 3. Pushing to GitHub

To link and push to a remote GitHub repository:

```bash
# Add remote origin
git remote add origin https://github.com/<your-organization-or-username>/SIH26083-Heat-Risk.git

# Push main branch
git push -u origin main
```

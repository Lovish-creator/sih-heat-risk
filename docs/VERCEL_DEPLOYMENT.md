# Vercel Deployment Guide - ThermoShield India (SIH26083)

This guide provides step-by-step instructions for deploying the **ThermoShield India** FastAPI + Leaflet web application to **Vercel** serverless cloud infrastructure.

---

## 1. Prerequisites

1. A **GitHub account** with access to the repository: `https://github.com/Lovish-creator/sih-heat-risk.git`.
2. A **Vercel account** (free tier supported): [https://vercel.com/signup](https://vercel.com/signup).

---

## 2. Serverless Architecture Overview

ThermoShield India uses a hybrid serverless deployment architecture on Vercel:

* **Entrypoint (`api/index.py`):** ASGI bridge exposing the FastAPI application (`backend.app.main:app`) as a serverless microservice.
* **Routing (`vercel.json`):** Rewrites all incoming web requests (`/(.*)`) to the ASGI handler (`/api/index.py`).
* **Static Assets:** The HTML, CSS, JavaScript, and GIS GeoJSON files in `frontend/` and `data/` are dynamically bundled into the serverless function runtime.

---

## 3. Deployment Method A: GitHub Repository Sync (Recommended)

1. Log in to your [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **"Add New..."** -> **"Project"**.
3. Under **"Import Git Repository"**, select `sih-heat-risk` (or `Lovish-creator/sih-heat-risk`).
4. In the configuration modal:
   - **Project Name:** `thermoshield-india` (or your preferred name)
   - **Framework Preset:** `Other` (Vercel will automatically detect Python via `vercel.json`)
   - **Root Directory:** `./`
   - **Build Command:** *(Leave blank)*
   - **Output Directory:** *(Leave blank)*
5. Click **"Deploy"**.

Vercel will install dependencies from `requirements.txt`, package `api/index.py`, and provision a globally distributed HTTPS domain (e.g., `https://thermoshield-india.vercel.app`).

---

## 4. Deployment Method B: Vercel CLI

If deploying directly from your local terminal:

```bash
# 1. Install Vercel CLI globally
npm install -g vercel

# 2. Login to your Vercel account
vercel login

# 3. Deploy from repository root
vercel

# 4. Deploy to production
vercel --prod
```

---

## 5. Verification Checklist Post-Deployment

Once deployed, verify the following endpoints on your live Vercel URL:

| Endpoint | Target URL | Expected Response |
| :--- | :--- | :--- |
| **Frontend UI** | `https://<your-project>.vercel.app/` | Status `200 OK` (Interactive Leaflet Map + Dashboard) |
| **API Docs** | `https://<your-project>.vercel.app/docs` | Status `200 OK` (Interactive OpenAPI Swagger UI) |
| **Health Check** | `https://<your-project>.vercel.app/health` | `{"status": "healthy", ...}` |
| **GIS Map Risk** | `https://<your-project>.vercel.app/api/v1/map/risk?city=delhi` | `{"type": "FeatureCollection", "features": [290 items]}` |
| **Biometeorology**| `https://<your-project>.vercel.app/api/v1/thermal/current?city=mumbai` | `{"thermal_analysis": {"metrics": {"heat_index": ...}}}` |

---

## 6. Environment Variables (Optional)

All core Tier-1 functionality operates with zero API keys using open government and open meteorology endpoints.

If configuring custom rate limits or logging:
* `ENVIRONMENT`: `production`
* `LOG_LEVEL`: `INFO`
* `CACHE_TTL_SECONDS`: `300`

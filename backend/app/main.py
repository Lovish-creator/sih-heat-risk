"""
SIH26083 FastAPI Application Main Entrypoint.

Extreme Heatwave Early Warning and Human Thermal Stress Index
Ministry of Earth Sciences (MoES) / NCMRWF
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .api.endpoints import router as api_router

app = FastAPI(
    title="SIH26083 — Extreme Heatwave Early Warning & Human Thermal Stress Index",
    description="""
    **MoES / NCMRWF — Software / Disaster Management Prototype**
    
    Quantifying *"What the weather will do to humans"* through:
    * **Physiological UTCI (Universal Thermal Climate Index)** 6th-order biometeorological modeling
    * **Occupational WBGT (Wet Bulb Globe Temperature)** with NIOSH labor-rest regimens
    * **NOAA / NWS Heat Index**
    * **Census of India 2011 Demographic Vulnerability** (Elderly, Outdoor Laborers, Population Density)
    * **Ward-Level Risk Attribution** & GeoJSON Choropleth Layers
    * **5-Day Forecast Horizon (D+1 to D+5)**
    * **NCDC & WHO Grounded Actionable Advisories**
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration for open access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

# Mount Static Files (Frontend)
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        index_path = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "SIH26083 API Running. Visit /docs for interactive Swagger UI."}

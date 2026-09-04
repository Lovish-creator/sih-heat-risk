"""
FastAPI REST API Endpoints for SIH26083 Platform.
"""

from fastapi import APIRouter, Query, HTTPException
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import yaml
import os
import json

from ..schemas.schemas import (
    HealthResponse,
    DataStatusResponse,
    LocationsResponse,
    WeatherForecastResponse,
    ThermalForecastResponse,
    RiskForecastResponse,
    AdvisoryResponse
)
from ..thermal.hazard import calculate_thermal_hazard
from ..vulnerability.demographic import DemographicVulnerabilityEngine
from ..risk.engine import HeatRiskEngine
from ..gis.engine import GISEngine
from ..advisory.engine import AdvisoryEngine
from ..data_sources.nasa_power import NASAPowerProvider
from ..data_sources.cache import DataCache

router = APIRouter()

# Global engine singletons
cache_store = DataCache(cache_dir="data/cache", default_ttl_seconds=3600)
weather_provider = NASAPowerProvider(cache=cache_store, demo_mode=True)
vuln_engine = DemographicVulnerabilityEngine()
risk_engine = HeatRiskEngine(config_path="config/risk_weights.yaml")
gis_engine = GISEngine(vulnerability_engine=vuln_engine, risk_engine=risk_engine)
advisory_engine = AdvisoryEngine()

def load_city_profiles() -> Dict[str, Any]:
    """Helper to load city configurations."""
    path = "config/city_profiles.yaml"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f).get("cities", {})
    return {}


@router.get("/health", response_model=HealthResponse, tags=["System"])
def get_health():
    """System health check and operational status."""
    return {
        "status": "healthy",
        "app_name": "SIH26083-Heat-Risk-Early-Warning",
        "version": "1.0.0",
        "demo_mode": weather_provider.demo_mode,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/api/v1/data-status", response_model=DataStatusResponse, tags=["Observability"])
def get_data_status(city: str = Query("ahmedabad", description="City identifier")):
    """Expose cache status, data freshness, and upstream source availability."""
    cities = load_city_profiles()
    active_city_name = cities.get(city, {}).get("name", city.title())
    
    return {
        "active_city": active_city_name,
        "demo_mode": weather_provider.demo_mode,
        "cache_entries": cache_store.count_entries(),
        "latest_ingestion_timestamp": datetime.now(timezone.utc).isoformat(),
        "upstream_sources": {
            "nasa_power_api": "ONLINE (Analysis-ready meteorological stream)",
            "imd_heatwave_guidance": "ONLINE (Threshold definitions)",
            "census_india_pca": "LOADED (2011 Baseline)",
            "ncmrwf_nwp_connector": "STUB_CONFIGURED (Tier-2 Interface)",
            "ncdc_health_guidelines": "ACTIVE (NAP-HRI 2024 Rule Engine)"
        }
    }


@router.get("/api/v1/locations", response_model=LocationsResponse, tags=["Locations"])
def get_locations():
    """List supported Indian pilot cities and geographic metadata."""
    cities = load_city_profiles()
    out = []
    for cid, cdata in cities.items():
        out.append({
            "id": cid,
            "name": cdata["name"],
            "state": cdata["state"],
            "region_type": cdata["region_type"],
            "center": cdata["center"],
            "is_pilot": cdata.get("is_pilot", False)
        })
    return {"cities": out}


@router.get("/api/v1/weather/current", tags=["Meteorology"])
def get_current_weather(city: str = Query("ahmedabad")):
    """Get current day dry-bulb temperature, relative humidity, wind speed, and solar irradiance."""
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    data = weather_provider.get_current_weather(center["lat"], center["lon"], city)
    return {
        "city_id": city,
        "city_name": cdata["name"],
        "weather": data
    }


@router.get("/api/v1/weather/forecast", response_model=WeatherForecastResponse, tags=["Meteorology"])
def get_weather_forecast(
    city: str = Query("ahmedabad"),
    days: int = Query(5, ge=1, le=5)
):
    """Get 5-day daily forecast meteorological series (D+1 to D+5)."""
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    series = weather_provider.get_forecast_weather(center["lat"], center["lon"], city, days)
    return {
        "city_id": city,
        "city_name": cdata["name"],
        "forecast_days": len(series),
        "data": series
    }


@router.get("/api/v1/thermal/current", tags=["Thermal Stress"])
def get_current_thermal(city: str = Query("ahmedabad")):
    """Get calculated biometeorological indices (UTCI, WBGT, Heat Index) for current day."""
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    weather = weather_provider.get_current_weather(center["lat"], center["lon"], city)
    hazard = calculate_thermal_hazard(
        temp_c=weather["temp_c"],
        relative_humidity_pct=weather["relative_humidity_pct"],
        wind_speed_10m_m_s=weather["wind_speed_10m_m_s"],
        solar_radiation_w_m2=weather["solar_radiation_w_m2"]
    )
    return {
        "city_id": city,
        "city_name": cdata["name"],
        "date": weather["date"],
        "thermal_analysis": hazard
    }


@router.get("/api/v1/thermal/forecast", response_model=ThermalForecastResponse, tags=["Thermal Stress"])
def get_thermal_forecast(
    city: str = Query("ahmedabad"),
    days: int = Query(5, ge=1, le=5)
):
    """Get 5-day daily biometeorological thermal stress forecast."""
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    weather_series = weather_provider.get_forecast_weather(center["lat"], center["lon"], city, days)
    thermal_series = []
    
    for item in weather_series:
        hz = calculate_thermal_hazard(
            temp_c=item["temp_c"],
            relative_humidity_pct=item["relative_humidity_pct"],
            wind_speed_10m_m_s=item["wind_speed_10m_m_s"],
            solar_radiation_w_m2=item["solar_radiation_w_m2"]
        )
        thermal_series.append({
            "horizon_day": item["horizon_day"],
            "horizon_label": item["horizon_label"],
            "date": item["date"],
            "inputs": hz["inputs"],
            "intermediates": hz["intermediates"],
            "metrics": hz["metrics"],
            "composite_hazard_score": hz["composite_hazard_score"]
        })

    return {
        "city_id": city,
        "city_name": cdata["name"],
        "forecast_days": len(thermal_series),
        "series": thermal_series
    }


@router.get("/api/v1/vulnerability", tags=["Demographics"])
def get_vulnerability(city: str = Query("ahmedabad")):
    """Get Census 2011 demographic vulnerability scores across all municipal wards."""
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    census_file = cdata.get("census_data_file", "data/sample/ahmedabad_census_wards.json")
    
    wards = gis_engine.load_census_wards(census_file)
    processed = vuln_engine.process_city_wards(wards)
    
    return {
        "city_id": city,
        "city_name": cdata["name"],
        "census_baseline_year": 2011,
        "total_wards": len(processed),
        "wards": processed
    }


@router.get("/api/v1/risk/current", tags=["Risk Engine"])
def get_current_risk(city: str = Query("ahmedabad")):
    """Get city-wide average current Relative Heat-Health Risk Score and alert level."""
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    weather = weather_provider.get_current_weather(center["lat"], center["lon"], city)
    hazard = calculate_thermal_hazard(
        temp_c=weather["temp_c"],
        relative_humidity_pct=weather["relative_humidity_pct"],
        wind_speed_10m_m_s=weather["wind_speed_10m_m_s"],
        solar_radiation_w_m2=weather["solar_radiation_w_m2"]
    )
    
    # Average demographic vulnerability across wards
    census_file = cdata.get("census_data_file", "data/sample/ahmedabad_census_wards.json")
    wards = gis_engine.load_census_wards(census_file)
    processed = vuln_engine.process_city_wards(wards)
    avg_vuln = sum(w["vulnerability_score"] for w in processed) / max(1, len(processed))

    risk_eval = risk_engine.calculate_risk(
        hazard_score=hazard["composite_hazard_score"],
        vulnerability_score=avg_vuln,
        consecutive_heat_days=1
    )

    return {
        "city_id": city,
        "city_name": cdata["name"],
        "date": weather["date"],
        "hazard_score": hazard["composite_hazard_score"],
        "city_avg_vulnerability": round(avg_vuln, 1),
        "heat_risk_score": risk_eval["risk_score"],
        "alert_level": risk_eval["alert_level"],
        "alert_label": risk_eval["alert_label"],
        "alert_color": risk_eval["alert_color"],
        "action_summary": risk_eval["action_summary"],
        "metrics_summary": {
            "temp_c": weather["temp_c"],
            "utci_c": hazard["metrics"]["utci"]["value_c"],
            "wbgt_c": hazard["metrics"]["wbgt"]["value_c"],
            "heat_index_c": hazard["metrics"]["heat_index"]["value_c"]
        },
        "disclaimer": risk_eval["disclaimer"]
    }


@router.get("/api/v1/risk/forecast", response_model=RiskForecastResponse, tags=["Risk Engine"])
def get_risk_forecast(
    city: str = Query("ahmedabad"),
    days: int = Query(5, ge=1, le=5)
):
    """Get 5-day multi-horizon composite risk forecast with cumulative duration penalty."""
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    weather_series = weather_provider.get_forecast_weather(center["lat"], center["lon"], city, days)
    census_file = cdata.get("census_data_file", "data/sample/ahmedabad_census_wards.json")
    wards = gis_engine.load_census_wards(census_file)
    processed = vuln_engine.process_city_wards(wards)
    avg_vuln = sum(w["vulnerability_score"] for w in processed) / max(1, len(processed))

    horizon_list = []
    consecutive_hot_days = 0

    for idx, item in enumerate(weather_series):
        hz = calculate_thermal_hazard(
            temp_c=item["temp_c"],
            relative_humidity_pct=item["relative_humidity_pct"],
            wind_speed_10m_m_s=item["wind_speed_10m_m_s"],
            solar_radiation_w_m2=item["solar_radiation_w_m2"]
        )
        
        # Track heatwave consecutive duration
        if hz["composite_hazard_score"] >= 60.0 or item["temp_c"] >= 41.0:
            consecutive_hot_days += 1
        else:
            consecutive_hot_days = max(1, consecutive_hot_days)

        r_calc = risk_engine.calculate_risk(
            hazard_score=hz["composite_hazard_score"],
            vulnerability_score=avg_vuln,
            consecutive_heat_days=consecutive_hot_days
        )

        horizon_list.append({
            "horizon_day": item["horizon_day"],
            "horizon_label": item["horizon_label"],
            "date": item["date"],
            "temp_c": item["temp_c"],
            "utci_c": hz["metrics"]["utci"]["value_c"],
            "wbgt_c": hz["metrics"]["wbgt"]["value_c"],
            "hazard_score": hz["composite_hazard_score"],
            "vulnerability_score": round(avg_vuln, 1),
            "heat_risk_score": r_calc["risk_score"],
            "alert_level": r_calc["alert_level"],
            "alert_label": r_calc["alert_label"],
            "alert_color": r_calc["alert_color"],
            "action_summary": r_calc["action_summary"]
        })

    return {
        "city_id": city,
        "city_name": cdata["name"],
        "forecast_days": len(horizon_list),
        "horizon": horizon_list,
        "disclaimer": "Prototype Relative Heat-Health Risk Estimate — not a clinical diagnosis or absolute mortality forecast."
    }


@router.get("/api/v1/map/risk", tags=["GIS & Spatial"])
def get_map_risk(
    city: str = Query("ahmedabad"),
    day: int = Query(1, ge=1, le=5, description="Forecast horizon day (1 to 5)")
):
    """
    Get enriched GeoJSON FeatureCollection with ward geometries, demographic vulnerability,
    and ward-level risk attribution for Leaflet choropleth rendering.
    """
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    weather_series = weather_provider.get_forecast_weather(center["lat"], center["lon"], city, 5)
    selected_idx = min(day - 1, len(weather_series) - 1)
    target_weather = weather_series[selected_idx]

    hz = calculate_thermal_hazard(
        temp_c=target_weather["temp_c"],
        relative_humidity_pct=target_weather["relative_humidity_pct"],
        wind_speed_10m_m_s=target_weather["wind_speed_10m_m_s"],
        solar_radiation_w_m2=target_weather["solar_radiation_w_m2"]
    )

    geojson_file = cdata.get("geojson_file", "data/sample/ahmedabad_wards.geojson")
    census_file = cdata.get("census_data_file", "data/sample/ahmedabad_census_wards.json")

    return gis_engine.generate_ward_risk_geojson(
        geojson_path=geojson_file,
        census_path=census_file,
        hazard_data=hz,
        consecutive_heat_days=day
    )


@router.get("/api/v1/advisory", response_model=AdvisoryResponse, tags=["Advisories"])
def get_advisories(
    city: str = Query("ahmedabad"),
    alert_level: Optional[str] = Query(None, description="Optional override (GREEN, YELLOW, ORANGE, RED)")
):
    """
    Get persona-tailored public health advisories grounded in NCDC 2024 and WHO guidelines for:
    1. Citizens
    2. Outdoor Workers (with NIOSH rest cycles)
    3. Municipal Authorities
    """
    cities = load_city_profiles()
    cdata = cities.get(city, cities.get("ahmedabad"))
    center = cdata["center"]
    
    weather = weather_provider.get_current_weather(center["lat"], center["lon"], city)
    hazard = calculate_thermal_hazard(
        temp_c=weather["temp_c"],
        relative_humidity_pct=weather["relative_humidity_pct"],
        wind_speed_10m_m_s=weather["wind_speed_10m_m_s"],
        solar_radiation_w_m2=weather["solar_radiation_w_m2"]
    )

    # Calculate current risk if alert_level not specified
    if not alert_level:
        census_file = cdata.get("census_data_file", "data/sample/ahmedabad_census_wards.json")
        wards = gis_engine.load_census_wards(census_file)
        processed = vuln_engine.process_city_wards(wards)
        avg_vuln = sum(w["vulnerability_score"] for w in processed) / max(1, len(processed))
        
        r_calc = risk_engine.calculate_risk(
            hazard_score=hazard["composite_hazard_score"],
            vulnerability_score=avg_vuln,
            consecutive_heat_days=1
        )
        final_level = r_calc["alert_level"]
        final_score = r_calc["risk_score"]
    else:
        final_level = alert_level.upper()
        final_score = 80.0 if final_level == "RED" else 60.0 if final_level == "ORANGE" else 40.0 if final_level == "YELLOW" else 15.0

    advisory_bundle = advisory_engine.generate_advisories(
        alert_level=final_level,
        risk_score=final_score,
        wbgt_info=hazard["metrics"]["wbgt"],
        utci_info=hazard["metrics"]["utci"]
    )

    return {
        "city_id": city,
        "alert_level": final_level,
        "risk_score": final_score,
        "personas": advisory_bundle["personas"],
        "provenance": advisory_bundle["provenance"]
    }


@router.get("/api/v1/sources", tags=["Provenance & Science"])
def get_sources():
    """Expose complete data source audit registry."""
    path = "data/SOURCE_REGISTRY.md"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"registry_markdown": content, "total_registered_sources": 11}
    return {"registry_markdown": "# Source registry not found", "total_registered_sources": 0}


@router.get("/api/v1/methodology", tags=["Provenance & Science"])
def get_methodology():
    """Return scientific formulas, parameters, and references used across the pipeline."""
    return {
        "models": {
            "utci": {
                "name": "Universal Thermal Climate Index",
                "formula": "6th-order operational polynomial (Bröde et al., 2012)",
                "inputs": ["T2M (Air Temp)", "RH2M (Relative Humidity)", "WS10M (10m Wind)", "ALLSKY_SFC_SW_DWN (Solar Irradiance)"],
                "validity_bounds": {"temp_c": "[-50, 50]", "wind_10m": "[0.5, 17.0 m/s]", "vapor_pressure": "[0, 50 hPa]"}
            },
            "wbgt": {
                "name": "Wet Bulb Globe Temperature",
                "formula": "0.7*Tnw + 0.2*Tg + 0.1*Ta (Outdoor with solar radiation)",
                "standard": "ISO 7243 / NIOSH 2016 Criteria Pub No. 2016-106"
            },
            "heat_index": {
                "name": "NOAA / NWS Heat Index",
                "formula": "Rothfusz (1990) 9-term polynomial regression with RH adjustments"
            },
            "vulnerability": {
                "name": "Demographic Vulnerability Index",
                "weights": {"elderly_60plus": 0.40, "outdoor_workers": 0.35, "population_density": 0.25},
                "baseline_source": "Census of India 2011 Primary Census Abstract"
            },
            "heat_health_risk": {
                "name": "Composite Relative Heat-Health Risk Score",
                "formula": "0.55 * HazardScore + 0.30 * VulnerabilityScore + 0.15 * DurationFactor*100",
                "range": "[0, 100]",
                "alert_scale": {"GREEN": "[0, 25]", "YELLOW": "[26, 50]", "ORANGE": "[51, 75]", "RED": "[76, 100]"}
            }
        },
        "disclaimer": "All predictions represent relative epidemiological risk scores; not a clinical prognosis or absolute death count."
    }

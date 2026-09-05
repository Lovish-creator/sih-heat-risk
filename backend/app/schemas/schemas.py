"""
Pydantic API Schemas for Request & Response Data Contracts.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    demo_mode: bool
    timestamp: str


class DataStatusResponse(BaseModel):
    active_city: str
    demo_mode: bool
    cache_entries: int
    latest_ingestion_timestamp: str
    upstream_sources: Dict[str, str]


class CityProfileSchema(BaseModel):
    id: str
    name: str
    state: str
    region_type: str
    center: Dict[str, float]
    is_pilot: bool


class LocationsResponse(BaseModel):
    cities: List[CityProfileSchema]


class WeatherObservation(BaseModel):
    horizon_day: int
    horizon_label: str
    date: str
    temp_c: float
    relative_humidity_pct: float
    wind_speed_10m_m_s: float
    solar_radiation_w_m2: float
    condition_summary: Optional[str] = None
    provider: str
    is_demo_data: bool


class WeatherForecastResponse(BaseModel):
    city_id: str
    city_name: str
    forecast_days: int
    data: List[WeatherObservation]


class ThermalMetricDetail(BaseModel):
    value_c: float
    category: Optional[str] = None
    risk_level: Optional[str] = None
    color: str
    hazard_score: float
    description: str


class ThermalAnalysisResponse(BaseModel):
    horizon_day: int
    horizon_label: str
    date: str
    inputs: Dict[str, Any]
    intermediates: Dict[str, Any]
    metrics: Dict[str, Any]
    composite_hazard_score: float


class ThermalForecastResponse(BaseModel):
    city_id: str
    city_name: str
    forecast_days: int
    series: List[ThermalAnalysisResponse]


class RiskForecastItem(BaseModel):
    horizon_day: int
    horizon_label: str
    date: str
    temp_c: float
    utci_c: float
    wbgt_c: float
    hazard_score: float
    vulnerability_score: float
    heat_risk_score: float
    alert_level: str
    alert_label: str
    alert_color: str
    action_summary: str


class RiskForecastResponse(BaseModel):
    city_id: str
    city_name: str
    forecast_days: int
    horizon: List[RiskForecastItem]
    disclaimer: str


class AdvisoryResponse(BaseModel):
    city_id: str
    alert_level: str
    risk_score: float
    personas: Dict[str, Any]
    provenance: Dict[str, Any]


class ThermalCalculateRequest(BaseModel):
    temp_c: float = Field(..., description="Dry-bulb air temperature in Celsius")
    relative_humidity_pct: float = Field(..., description="Relative humidity percentage (0-100%)")
    wind_speed_10m_m_s: float = Field(1.5, description="10m wind speed in m/s")
    solar_radiation_w_m2: float = Field(0.0, description="Shortwave solar radiation flux in W/m²")


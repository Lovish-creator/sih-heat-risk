"""
Pydantic V2 API Schemas for Request & Response Data Contracts.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    demo_mode: bool
    timestamp: str
    database_status: Optional[str] = "ONLINE"


class DataFreshnessResponse(BaseModel):
    last_updated_utc: str
    minutes_ago: float
    status: str
    active_providers: Dict[str, str]
    fallback_active: bool
    fallback_policy: str


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
    district: Optional[str] = None
    region_type: str
    center: Dict[str, float]
    total_wards: Optional[int] = 50
    is_pilot: bool


class LocationsResponse(BaseModel):
    cities: List[CityProfileSchema]
    total_cities: int


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
    temp_c: Optional[float] = Field(None, description="Dry-bulb air temperature in Celsius")
    relative_humidity_pct: Optional[float] = Field(None, description="Relative humidity percentage (0-100%)")
    wind_speed_10m_m_s: Optional[float] = Field(1.5, description="10m wind speed in m/s")
    solar_radiation_w_m2: Optional[float] = Field(0.0, description="Shortwave solar radiation flux in W/m2")
    air_temperature: Optional[float] = Field(None, description="Alias for temp_c")
    relative_humidity: Optional[float] = Field(None, description="Alias for relative_humidity_pct")
    wind_speed: Optional[float] = Field(None, description="Alias for wind_speed_10m_m_s")
    solar_radiation: Optional[float] = Field(None, description="Alias for solar_radiation_w_m2")

    def get_resolved_values(self) -> tuple[float, float, float, float]:
        t = self.temp_c if self.temp_c is not None else (self.air_temperature if self.air_temperature is not None else 35.0)
        rh = self.relative_humidity_pct if self.relative_humidity_pct is not None else (self.relative_humidity if self.relative_humidity is not None else 50.0)
        ws = self.wind_speed_10m_m_s if self.wind_speed_10m_m_s is not None else (self.wind_speed if self.wind_speed is not None else 1.5)
        sr = self.solar_radiation_w_m2 if self.solar_radiation_w_m2 is not None else (self.solar_radiation if self.solar_radiation is not None else 0.0)
        return t, rh, ws, sr


class AlertTestRequest(BaseModel):
    city_name: str = "Abohar"
    ward_name: str = "Ward 1 - Main Bazaar"
    risk_score: float = 82.5
    alert_level: str = "RED"
    webhook_url: Optional[str] = "https://mock.ndma.gov.in/eoc/webhook"


class AlertTestResponse(BaseModel):
    status: str
    alert_payload: Dict[str, Any]
    dispatch_result: Dict[str, Any]

"""
Normalized Relational Data Models for SIH26083 Platform.
"""

from sqlalchemy import (
    Integer, String, Float, Boolean, DateTime, ForeignKey, 
    Text, UniqueConstraint, JSON
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional
from ..base import Base


class LocationModel(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    state: Mapped[str] = mapped_column(String(64), nullable=False)
    district: Mapped[str] = mapped_column(String(64), nullable=False)
    center_lat: Mapped[float] = mapped_column(Float, nullable=False)
    center_lon: Mapped[float] = mapped_column(Float, nullable=False)
    radius_km: Mapped[float] = mapped_column(Float, default=5.0)
    region_type: Mapped[str] = mapped_column(String(64), default="Urban Core")
    is_pilot: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    wards = relationship("WardModel", back_populates="location", cascade="all, delete-orphan")
    weather_observations = relationship("WeatherObservationModel", back_populates="location")
    weather_forecasts = relationship("WeatherForecastModel", back_populates="location")


class WardModel(Base):
    __tablename__ = "wards"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)  # e.g. "abohar_ward_1"
    location_id: Mapped[str] = mapped_column(String(64), ForeignKey("locations.id"), nullable=False, index=True)
    ward_number: Mapped[int] = mapped_column(Integer, nullable=False)
    ward_name: Mapped[str] = mapped_column(String(128), nullable=False)
    zone_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    lcz_class: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    center_lat: Mapped[float] = mapped_column(Float, nullable=False)
    center_lon: Mapped[float] = mapped_column(Float, nullable=False)
    area_sqkm: Mapped[float] = mapped_column(Float, default=1.0)
    
    # GeoJSON representation & Truthfulness Flags
    geometry_geojson: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_official_geometry: Mapped[bool] = mapped_column(Boolean, default=False)
    is_generated_geometry: Mapped[bool] = mapped_column(Boolean, default=True)
    geometry_source: Mapped[str] = mapped_column(String(256), default="Delimitation / Synthetic LCZ")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    location = relationship("LocationModel", back_populates="wards")
    demographics = relationship("DemographicModel", back_populates="ward", uselist=False, cascade="all, delete-orphan")
    thermal_indices = relationship("ThermalIndexModel", back_populates="ward")
    risk_scores = relationship("RiskScoreModel", back_populates="ward")

    __table_args__ = (
        UniqueConstraint("location_id", "ward_number", name="uq_location_ward_number"),
    )


class DemographicModel(Base):
    __tablename__ = "demographics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[str] = mapped_column(String(128), ForeignKey("wards.id"), nullable=False, unique=True, index=True)
    tot_pop: Mapped[int] = mapped_column(Integer, nullable=False)
    pop_elderly_60plus: Mapped[int] = mapped_column(Integer, default=0)
    elderly_percentage: Mapped[float] = mapped_column(Float, default=8.0)
    workers_outdoor: Mapped[int] = mapped_column(Integer, default=0)
    outdoor_worker_percentage: Mapped[float] = mapped_column(Float, default=25.0)
    pop_density_per_sqkm: Mapped[float] = mapped_column(Float, default=1000.0)
    vulnerability_score: Mapped[float] = mapped_column(Float, default=50.0)
    
    # Provenance metadata
    source: Mapped[str] = mapped_column(String(256), default="Census of India 2011 PCA")
    source_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    source_year: Mapped[int] = mapped_column(Integer, default=2011)
    is_fallback: Mapped[bool] = mapped_column(Boolean, default=False)
    fallback_reason: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    ward = relationship("WardModel", back_populates="demographics")


class WeatherObservationModel(Base):
    __tablename__ = "weather_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[str] = mapped_column(String(64), ForeignKey("locations.id"), nullable=False, index=True)
    observation_time_utc: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    relative_humidity_pct: Mapped[float] = mapped_column(Float, nullable=False)
    dew_point_c: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    wind_speed_10m_m_s: Mapped[float] = mapped_column(Float, default=1.0)
    wind_direction_deg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    solar_radiation_w_m2: Mapped[float] = mapped_column(Float, default=0.0)
    uv_index: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    provider: Mapped[str] = mapped_column(String(64), default="open-meteo")
    quality_flag: Mapped[str] = mapped_column(String(32), default="VALID")
    is_fallback: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    location = relationship("LocationModel", back_populates="weather_observations")

    __table_args__ = (
        UniqueConstraint("location_id", "observation_time_utc", "provider", name="uq_location_time_provider"),
    )


class WeatherForecastModel(Base):
    __tablename__ = "weather_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[str] = mapped_column(String(64), ForeignKey("locations.id"), nullable=False, index=True)
    forecast_generated_at_utc: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    valid_time_utc: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    horizon_day: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 5
    temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    relative_humidity_pct: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed_10m_m_s: Mapped[float] = mapped_column(Float, default=1.0)
    solar_radiation_w_m2: Mapped[float] = mapped_column(Float, default=0.0)
    provider: Mapped[str] = mapped_column(String(64), default="open-meteo")
    is_fallback: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    location = relationship("LocationModel", back_populates="weather_forecasts")


class RadiationObservationModel(Base):
    __tablename__ = "radiation_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[str] = mapped_column(String(64), ForeignKey("locations.id"), nullable=False, index=True)
    timestamp_utc: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    allsky_sfc_sw_dwn_w_m2: Mapped[float] = mapped_column(Float, nullable=False)
    clear_sky_sw_w_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    provider: Mapped[str] = mapped_column(String(64), default="nasa-power")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class ThermalIndexModel(Base):
    __tablename__ = "thermal_indices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[Optional[str]] = mapped_column(String(128), ForeignKey("wards.id"), nullable=True, index=True)
    location_id: Mapped[str] = mapped_column(String(64), ForeignKey("locations.id"), nullable=False, index=True)
    calculation_time_utc: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    utci_c: Mapped[float] = mapped_column(Float, nullable=False)
    utci_category: Mapped[str] = mapped_column(String(64), nullable=False)
    wbgt_c: Mapped[float] = mapped_column(Float, nullable=False)
    wbgt_category: Mapped[str] = mapped_column(String(64), nullable=False)
    heat_index_c: Mapped[float] = mapped_column(Float, nullable=False)
    thermal_hazard_score: Mapped[float] = mapped_column(Float, nullable=False)
    engine_version: Mapped[str] = mapped_column(String(32), default="1.2.0-scientific")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    ward = relationship("WardModel", back_populates="thermal_indices")


class RiskScoreModel(Base):
    __tablename__ = "risk_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ward_id: Mapped[str] = mapped_column(String(128), ForeignKey("wards.id"), nullable=False, index=True)
    horizon_day: Mapped[int] = mapped_column(Integer, default=1)
    valid_time_utc: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    thermal_hazard_score: Mapped[float] = mapped_column(Float, nullable=False)
    demographic_vulnerability_score: Mapped[float] = mapped_column(Float, nullable=False)
    heatwave_duration_days: Mapped[int] = mapped_column(Integer, default=1)
    persistence_score: Mapped[float] = mapped_column(Float, default=0.0)
    heat_risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    alert_level: Mapped[str] = mapped_column(String(16), nullable=False)  # GREEN, YELLOW, ORANGE, RED
    model_version: Mapped[str] = mapped_column(String(32), default="baseline-0.2")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    ward = relationship("WardModel", back_populates="risk_scores")


class AdvisoryModel(Base):
    __tablename__ = "advisories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alert_level: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    persona: Mapped[str] = mapped_column(String(32), nullable=False)  # general_public, outdoor_workers, authorities
    advisory_text: Mapped[str] = mapped_column(Text, nullable=False)
    authority_guideline_ref: Mapped[str] = mapped_column(String(128), default="NAP-HRI 2024 / WHO")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataSourceModel(Base):
    __tablename__ = "data_sources"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    official_url: Mapped[str] = mapped_column(String(256), nullable=False)
    organization: Mapped[str] = mapped_column(String(128), nullable=False)
    tier: Mapped[str] = mapped_column(String(32), default="Tier 1")
    status: Mapped[str] = mapped_column(String(32), default="ONLINE")
    last_sync_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class IngestionRunModel(Base):
    __tablename__ = "ingestion_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="RUNNING")
    records_ingested: Mapped[int] = mapped_column(Integer, default=0)
    errors_count: Mapped[int] = mapped_column(Integer, default=0)
    log_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ModelVersionModel(Base):
    __tablename__ = "model_versions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    model_name: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    parameters_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class HealthRecordModel(Base):
    __tablename__ = "health_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[str] = mapped_column(String(64), ForeignKey("locations.id"), nullable=False, index=True)
    record_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    heat_related_cases: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    hospital_admissions: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mortality_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    data_source: Mapped[str] = mapped_column(String(128), nullable=False)
    source_year: Mapped[int] = mapped_column(Integer, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

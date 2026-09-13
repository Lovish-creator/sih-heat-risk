"""
Centralized Application Configuration.
Loads environment variables using pydantic-settings with explicit fallback policies.
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from .constants import AppEnv, DataMode


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "SIH26083-ThermoShield-India"
    APP_VERSION: str = "2.0.0-modular"
    APP_ENV: AppEnv = AppEnv.DEMO
    DATA_MODE: DataMode = DataMode.HYBRID
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    ENABLE_FALLBACK_DATA: bool = True
    ENABLE_EXTERNAL_INGESTION: bool = True
    INGESTION_INTERVAL_MINUTES: int = 60

    DATABASE_URL: str = Field(
        default="sqlite:///./data/heat_risk.db",
        description="SQLAlchemy Database Connection URI"
    )
    DB_ECHO: bool = False

    CORS_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str = "sih26083-insecure-default-secret-change-in-production"

    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    NASA_POWER_BASE_URL: str = "https://power.larc.nasa.gov/api/temporal/hourly/point"
    NOMINATIM_BASE_URL: str = "https://nominatim.openstreetmap.org"
    NOMINATIM_USER_AGENT: str = "SIH26083-ThermoShield-India/2.0 (moes-ncmrwf-prototype)"

    CONFIG_DIR: str = Field(default="config")
    DATA_DIR: str = Field(default="data")
    RISK_WEIGHTS_FILE: str = "config/risk_weights.yaml"
    CITY_PROFILES_FILE: str = "config/city_profiles.yaml"
    THRESHOLDS_FILE: str = "config/thresholds.yaml"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == AppEnv.PRODUCTION

    @property
    def is_demo(self) -> bool:
        return self.APP_ENV == AppEnv.DEMO or self.DATA_MODE == DataMode.DEMO

    def should_allow_fallbacks(self) -> bool:
        if self.is_production:
            return False
        return self.ENABLE_FALLBACK_DATA


settings = Settings()

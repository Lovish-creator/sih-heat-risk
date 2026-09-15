"""
Centralized Application Configuration.
Loads environment variables using pydantic-settings with explicit fallback policies.
Robust against empty string environment variables commonly injected by cloud dashboards.
"""

import os
from typing import List, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from .constants import AppEnv, DataMode

# Pre-sanitize environment variables if they are set to empty strings in cloud environments
for _k in [
    "APP_ENV", "DATA_MODE", "DEBUG", "LOG_LEVEL",
    "ENABLE_FALLBACK_DATA", "ENABLE_EXTERNAL_INGESTION",
    "INGESTION_INTERVAL_MINUTES", "DATABASE_URL", "DB_ECHO"
]:
    if _k in os.environ and os.environ[_k].strip() == "":
        del os.environ[_k]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "SIH26083-Taapamigo-India"
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
    NOMINATIM_USER_AGENT: str = "SIH26083-Taapamigo-India/2.0 (moes-ncmrwf-prototype)"

    CONFIG_DIR: str = Field(default="config")
    DATA_DIR: str = Field(default="data")
    RISK_WEIGHTS_FILE: str = "config/risk_weights.yaml"
    CITY_PROFILES_FILE: str = "config/city_profiles.yaml"
    THRESHOLDS_FILE: str = "config/thresholds.yaml"

    @field_validator("APP_ENV", mode="before")
    @classmethod
    def validate_app_env(cls, v: Any) -> AppEnv:
        if not v or (isinstance(v, str) and not v.strip()):
            return AppEnv.DEMO
        if isinstance(v, str):
            v_clean = v.strip().lower()
            for env in AppEnv:
                if env.value.lower() == v_clean:
                    return env
        return v

    @field_validator("DEBUG", "DB_ECHO", "ENABLE_FALLBACK_DATA", "ENABLE_EXTERNAL_INGESTION", mode="before")
    @classmethod
    def validate_bool(cls, v: Any) -> bool:
        if v is None or v == "" or (isinstance(v, str) and not v.strip()):
            return False
        if isinstance(v, str):
            return v.strip().lower() in ("true", "1", "yes", "on")
        return bool(v)

    @field_validator("DATA_MODE", mode="before")
    @classmethod
    def validate_data_mode(cls, v: Any) -> DataMode:
        if not v or (isinstance(v, str) and not v.strip()):
            return DataMode.HYBRID
        if isinstance(v, str):
            v_clean = v.strip().lower()
            for mode in DataMode:
                if mode.value.lower() == v_clean:
                    return mode
        return v

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

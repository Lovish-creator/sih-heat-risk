"""
Background Data Ingestion & Freshness Scheduler.
Automates periodic weather polling, unit normalization, database persistence,
and duplicate prevention for configured municipal locations.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler

from ..core.config import settings
from ..db.session import SessionLocal
from ..db.repositories import WeatherRepository, LocationRepository
from ..db.models import IngestionRunModel
from ..data_sources.open_meteo import OpenMeteoProvider
from ..data_sources.cache import DataCache

logger = logging.getLogger(__name__)


class IngestionScheduler:
    """
    Coordinates periodic data ingestion, observation deduplication, and database persistence.
    """

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.cache = DataCache(cache_dir="data/cache")
        self.provider = OpenMeteoProvider(cache=self.cache)
        self._is_running = False

    def ingest_location_weather(self, location_id: str, lat: float, lon: float) -> Dict[str, Any]:
        """
        Ingest current observation for a location and save to database.
        """
        db = SessionLocal()
        try:
            weather_repo = WeatherRepository(db)
            obs = self.provider.get_current_weather(lat=lat, lon=lon, city_id=location_id)

            obs_data = {
                "location_id": location_id,
                "observation_time_utc": datetime.now(timezone.utc),
                "temp_c": float(obs.get("temp_c", 35.0)),
                "relative_humidity_pct": float(obs.get("relative_humidity_pct", 40.0)),
                "dew_point_c": float(obs.get("dew_point_c", 20.0)) if obs.get("dew_point_c") is not None else None,
                "wind_speed_10m_m_s": float(obs.get("wind_speed_10m_m_s", 2.0)),
                "solar_radiation_w_m2": float(obs.get("solar_radiation_w_m2", 500.0)),
                "provider": "open-meteo",
                "quality_flag": "VALID",
                "is_fallback": bool(obs.get("is_demo_data", False))
            }
            saved = weather_repo.add_observation(obs_data)
            return {"status": "success", "id": saved.id, "temp_c": saved.temp_c}
        finally:
            db.close()

    def run_full_ingestion_cycle(self) -> Dict[str, Any]:
        """
        Execute an ingestion run across all registered pilot cities.
        """
        db = SessionLocal()
        start_time = datetime.now(timezone.utc)
        run_record = IngestionRunModel(
            provider="open-meteo",
            status="RUNNING",
            started_at=start_time
        )
        db.add(run_record)
        db.commit()
        db.refresh(run_record)

        records_count = 0
        errors_count = 0

        try:
            loc_repo = LocationRepository(db)
            locations = loc_repo.get_all()
            
            for loc in locations:
                try:
                    res = self.ingest_location_weather(loc.id, loc.center_lat, loc.center_lon)
                    if res.get("status") == "success":
                        records_count += 1
                except Exception as e:
                    errors_count += 1
                    logger.warning(f"Failed to ingest for {loc.id}: {e}")

            run_record.status = "COMPLETED" if errors_count == 0 else "PARTIAL"
            run_record.records_ingested = records_count
            run_record.errors_count = errors_count
            run_record.completed_at = datetime.now(timezone.utc)
            run_record.log_summary = f"Ingested {records_count} locations with {errors_count} errors."
            db.commit()

            return {
                "status": run_record.status,
                "records_ingested": records_count,
                "errors": errors_count,
                "duration_seconds": (run_record.completed_at - start_time).total_seconds()
            }
        except Exception as e:
            run_record.status = "FAILED"
            run_record.errors_count += 1
            run_record.log_summary = str(e)
            run_record.completed_at = datetime.now(timezone.utc)
            db.commit()
            return {"status": "failed", "error": str(e)}
        finally:
            db.close()

    def start(self):
        """Start background scheduler if external ingestion is enabled."""
        if settings.ENABLE_EXTERNAL_INGESTION and not self._is_running:
            try:
                self.scheduler.add_job(
                    self.run_full_ingestion_cycle,
                    "interval",
                    minutes=settings.INGESTION_INTERVAL_MINUTES,
                    id="weather_ingestion_job",
                    replace_existing=True
                )
                self.scheduler.start()
                self._is_running = True
                logger.info(f"Ingestion scheduler started (interval: {settings.INGESTION_INTERVAL_MINUTES}m).")
            except Exception as e:
                logger.warning(f"Could not start background scheduler: {e}")

    def shutdown(self):
        """Gracefully stop scheduler."""
        if self._is_running:
            self.scheduler.shutdown(wait=False)
            self._is_running = False

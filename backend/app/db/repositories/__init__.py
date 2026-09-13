"""
Database Repositories for Clean Data Access & CRUD Operations.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from ..models import (
    LocationModel, WardModel, DemographicModel,
    WeatherObservationModel, WeatherForecastModel,
    RadiationObservationModel, ThermalIndexModel,
    RiskScoreModel, AdvisoryModel, DataSourceModel,
    IngestionRunModel, ModelVersionModel, HealthRecordModel
)


class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, location_id: str) -> Optional[LocationModel]:
        return self.db.execute(select(LocationModel).where(LocationModel.id == location_id)).scalar_one_or_none()

    def get_all(self) -> List[LocationModel]:
        return list(self.db.execute(select(LocationModel).order_by(LocationModel.name)).scalars().all())

    def upsert(self, location_data: Dict[str, Any]) -> LocationModel:
        loc = self.get_by_id(location_data["id"])
        if not loc:
            loc = LocationModel(**location_data)
            self.db.add(loc)
        else:
            for k, v in location_data.items():
                setattr(loc, k, v)
        self.db.commit()
        self.db.refresh(loc)
        return loc


class WardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ward_id: str) -> Optional[WardModel]:
        return self.db.execute(select(WardModel).where(WardModel.id == ward_id)).scalar_one_or_none()

    def get_by_location(self, location_id: str) -> List[WardModel]:
        return list(self.db.execute(select(WardModel).where(WardModel.location_id == location_id).order_by(WardModel.ward_number)).scalars().all())

    def upsert_ward_with_demographics(self, ward_dict: Dict[str, Any], demo_dict: Dict[str, Any]) -> WardModel:
        ward = self.get_by_id(ward_dict["id"])
        if not ward:
            ward = WardModel(**ward_dict)
            self.db.add(ward)
            self.db.flush()
        else:
            for k, v in ward_dict.items():
                setattr(ward, k, v)

        # Upsert demographics
        if demo_dict:
            if not ward.demographics:
                demo_dict["ward_id"] = ward.id
                demo = DemographicModel(**demo_dict)
                self.db.add(demo)
            else:
                for k, v in demo_dict.items():
                    if k != "id" and k != "ward_id":
                        setattr(ward.demographics, k, v)
        
        self.db.commit()
        self.db.refresh(ward)
        return ward


class WeatherRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_observation(self, obs_data: Dict[str, Any]) -> WeatherObservationModel:
        # Check duplicate
        stmt = select(WeatherObservationModel).where(
            and_(
                WeatherObservationModel.location_id == obs_data["location_id"],
                WeatherObservationModel.observation_time_utc == obs_data["observation_time_utc"],
                WeatherObservationModel.provider == obs_data.get("provider", "open-meteo")
            )
        )
        existing = self.db.execute(stmt).scalar_one_or_none()
        if existing:
            for k, v in obs_data.items():
                setattr(existing, k, v)
            self.db.commit()
            return existing
        
        obs = WeatherObservationModel(**obs_data)
        self.db.add(obs)
        self.db.commit()
        self.db.refresh(obs)
        return obs

    def get_latest_observation(self, location_id: str) -> Optional[WeatherObservationModel]:
        stmt = select(WeatherObservationModel).where(
            WeatherObservationModel.location_id == location_id
        ).order_by(desc(WeatherObservationModel.observation_time_utc)).limit(1)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_forecast(self, location_id: str, days: int = 5) -> List[WeatherForecastModel]:
        stmt = select(WeatherForecastModel).where(
            and_(
                WeatherForecastModel.location_id == location_id,
                WeatherForecastModel.horizon_day <= days
            )
        ).order_by(WeatherForecastModel.horizon_day)
        return list(self.db.execute(stmt).scalars().all())


class DataSourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[DataSourceModel]:
        return list(self.db.execute(select(DataSourceModel).order_by(DataSourceModel.tier, DataSourceModel.name)).scalars().all())

    def upsert(self, source_dict: Dict[str, Any]) -> DataSourceModel:
        src = self.db.execute(select(DataSourceModel).where(DataSourceModel.id == source_dict["id"])).scalar_one_or_none()
        if not src:
            src = DataSourceModel(**source_dict)
            self.db.add(src)
        else:
            for k, v in source_dict.items():
                setattr(src, k, v)
        self.db.commit()
        self.db.refresh(src)
        return src

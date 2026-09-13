"""
Unit Tests for Database Models and Repositories.
"""

import pytest
from datetime import datetime, timezone
from backend.app.db.session import SessionLocal, init_db
from backend.app.db.repositories import (
    LocationRepository, WardRepository, WeatherRepository, DataSourceRepository
)
from backend.app.db.models import LocationModel, WardModel


@pytest.fixture(scope="module")
def db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()


def test_location_repository_crud(db):
    repo = LocationRepository(db)
    loc_data = {
        "id": "test_city",
        "name": "Test Municipal Corporation",
        "state": "Test State",
        "district": "Test District",
        "center_lat": 28.5,
        "center_lon": 77.2,
        "radius_km": 6.0,
        "region_type": "Municipal Corporation",
        "is_pilot": True
    }
    created = repo.upsert(loc_data)
    assert created.id == "test_city"
    assert created.name == "Test Municipal Corporation"

    fetched = repo.get_by_id("test_city")
    assert fetched is not None
    assert fetched.center_lat == 28.5


def test_ward_repository_with_demographics(db):
    loc_repo = LocationRepository(db)
    loc_repo.upsert({
        "id": "test_city_2",
        "name": "City 2",
        "state": "State 2",
        "district": "District 2",
        "center_lat": 20.0,
        "center_lon": 75.0
    })

    ward_repo = WardRepository(db)
    ward_dict = {
        "id": "test_city_2_ward_1",
        "location_id": "test_city_2",
        "ward_number": 1,
        "ward_name": "Ward 1 Central",
        "center_lat": 20.01,
        "center_lon": 75.01,
        "area_sqkm": 1.5,
        "is_official_geometry": True,
        "is_generated_geometry": False
    }
    demo_dict = {
        "tot_pop": 25000,
        "pop_elderly_60plus": 2500,
        "elderly_percentage": 10.0,
        "workers_outdoor": 7500,
        "outdoor_worker_percentage": 30.0,
        "pop_density_per_sqkm": 16666.0,
        "vulnerability_score": 62.5
    }

    ward = ward_repo.upsert_ward_with_demographics(ward_dict, demo_dict)
    assert ward.id == "test_city_2_ward_1"
    assert ward.demographics is not None
    assert ward.demographics.tot_pop == 25000


def test_weather_observation_duplicate_prevention(db):
    repo = WeatherRepository(db)
    loc_id = "test_city"
    now_utc = datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc)

    obs_1 = {
        "location_id": loc_id,
        "observation_time_utc": now_utc,
        "temp_c": 41.5,
        "relative_humidity_pct": 30.0,
        "wind_speed_10m_m_s": 2.5,
        "solar_radiation_w_m2": 800.0,
        "provider": "open-meteo"
    }

    saved_1 = repo.add_observation(obs_1)
    assert saved_1.temp_c == 41.5

    # Upsert same timestamp & provider -> must update without creating duplicate row
    obs_2 = {
        "location_id": loc_id,
        "observation_time_utc": now_utc,
        "temp_c": 42.0,  # updated reading
        "relative_humidity_pct": 28.0,
        "wind_speed_10m_m_s": 3.0,
        "solar_radiation_w_m2": 850.0,
        "provider": "open-meteo"
    }
    saved_2 = repo.add_observation(obs_2)
    assert saved_2.id == saved_1.id
    assert saved_2.temp_c == 42.0

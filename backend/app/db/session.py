"""
Database Engine and Session Management.
Supports SQLite (local testing) and PostgreSQL/PostGIS (production).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

from ..core.config import settings

# Configure engine kwargs based on dialect
connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    connect_args["check_same_thread"] = False
    # Ensure local sqlite directory exists
    os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", "")) or ".", exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DB_ECHO,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables if they do not exist (useful for zero-setup local dev & tests)."""
    from .base import Base
    from . import models  # Ensure all models are imported
    Base.metadata.create_all(bind=engine)

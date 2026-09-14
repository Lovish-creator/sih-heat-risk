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
db_url = settings.DATABASE_URL
if "sqlite" in db_url:
    connect_args["check_same_thread"] = False
    try:
        db_path = db_url.replace("sqlite:///", "")
        if db_path and not db_path.startswith(":"):
            db_dir = os.path.dirname(db_path) or "."
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
    except Exception:
        # Read-only filesystem (Vercel / Lambda) -> use /tmp
        db_url = "sqlite:////tmp/heat_risk.db"
        try:
            os.makedirs("/tmp", exist_ok=True)
        except Exception:
            db_url = "sqlite:///:memory:"

engine = create_engine(
    db_url,
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

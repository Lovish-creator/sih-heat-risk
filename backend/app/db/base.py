"""
SQLAlchemy Declarative Base.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass

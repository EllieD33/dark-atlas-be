from enum import unique

from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from app.db import Base
from datetime import datetime, timezone


class IOC(Base):
    __tablename__ = "iocs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    value = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    first_seen = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_seen = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    raw_data = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))

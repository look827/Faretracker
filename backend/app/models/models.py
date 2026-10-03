from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db import Base

class Monitor(Base):
    __tablename__ = "monitors"
    id = Column(Integer, primary_key=True)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    departure_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    airline = Column(String(100), nullable=True)
    stops = Column(Integer, nullable=True)
    target_price = Column(Numeric(12,2), nullable=True)
    drop_threshold_pct = Column(Numeric(6,2), default=5)
    increase_threshold_pct = Column(Numeric(6,2), default=10)
    large_drop_threshold_pct = Column(Numeric(6,2), default=10)
    frequency_minutes = Column(Integer, default=60)
    currency = Column(String(3), default="INR")
    timezone = Column(String(64), default="Asia/Kolkata")
    enabled = Column(Boolean, default=True)
    last_checked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    prices = relationship("FlightPrice", back_populates="monitor", cascade="all, delete-orphan")

class FlightPrice(Base):
    __tablename__ = "flight_prices"
    id = Column(Integer, primary_key=True)
    monitor_id = Column(Integer, ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False, index=True)
    airline = Column(String(100), nullable=True)
    flight_number = Column(String(32), nullable=True)
    stops = Column(Integer, nullable=True)
    departure_time = Column(DateTime(timezone=True), nullable=True)
    arrival_time = Column(DateTime(timezone=True), nullable=True)
    price = Column(Numeric(12,2), nullable=False)
    currency = Column(String(3), nullable=False)
    checked_at = Column(DateTime(timezone=True), nullable=False, index=True)
    source = Column(String(32), default="mock")
    monitor = relationship("Monitor", back_populates="prices")

class NotificationEvent(Base):
    __tablename__ = "notification_events"
    id = Column(Integer, primary_key=True)
    monitor_id = Column(Integer, ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False)
    channel = Column(String(32), nullable=False)
    event_type = Column(String(64), nullable=False)
    price_id = Column(Integer, nullable=False)
    event_key = Column(String(255), nullable=False, unique=True)
    sent_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    status = Column(String(32), default="sent")
    error = Column(String(500), nullable=True)

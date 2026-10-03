from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class MonitorCreate(BaseModel):
    origin: str = Field(min_length=3, max_length=3)
    destination: str = Field(min_length=3, max_length=3)
    departure_date: date
    return_date: Optional[date] = None
    airline: Optional[str] = None
    stops: Optional[int] = None
    target_price: Optional[Decimal] = None
    drop_threshold_pct: Decimal = 5
    increase_threshold_pct: Decimal = 10
    large_drop_threshold_pct: Decimal = 10
    frequency_minutes: int = 60
    currency: str = "INR"
    timezone: str = "Asia/Kolkata"
    enabled: bool = True

class MonitorOut(MonitorCreate):
    id: int
    last_checked_at: Optional[datetime] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PriceOut(BaseModel):
    id: int
    monitor_id: int
    airline: Optional[str]
    flight_number: Optional[str]
    stops: Optional[int]
    price: Decimal
    currency: str
    checked_at: datetime
    source: str
    model_config = ConfigDict(from_attributes=True)

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

@dataclass
class FlightQuote:
    airline: Optional[str]
    flight_number: Optional[str]
    stops: Optional[int]
    departure_time: Optional[datetime]
    arrival_time: Optional[datetime]
    price: Decimal
    currency: str
    source: str

class FlightDataProvider(ABC):
    @abstractmethod
    def search_flights(self, origin: str, destination: str, departure_date: date, return_date: Optional[date] = None, airline: Optional[str] = None, stops: Optional[int] = None) -> list[FlightQuote]:
        raise NotImplementedError

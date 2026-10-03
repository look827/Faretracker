import random
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from .base import FlightDataProvider, FlightQuote

class MockFlightDataProvider(FlightDataProvider):
    """Deterministic-ish test provider. Every returned quote is explicitly marked source='mock'."""
    def search_flights(self, origin, destination, departure_date, return_date=None, airline=None, stops=None):
        seed = hash((origin, destination, departure_date.isoformat(), return_date.isoformat() if return_date else "")) & 0xffffffff
        rng = random.Random(seed + int(datetime.utcnow().timestamp() // 3600))
        base = Decimal(rng.randrange(9000, 28001, 100))
        carrier = airline or rng.choice(["Air India Express", "IndiGo", "Air India"])
        stop_count = 0 if stops == 0 else (stops if stops is not None else rng.choice([0, 0, 1]))
        dep = datetime.combine(departure_date, time(rng.choice([5, 8, 11, 14, 18, 21]), rng.choice([0, 30])))
        arr = dep + timedelta(hours=3 + stop_count * 2)
        return [FlightQuote(carrier, f"MOCK-{rng.randint(100,999)}", stop_count, dep, arr, base, "INR", "mock")]

from decimal import Decimal
from statistics import median
from datetime import datetime, timedelta, timezone

def analyze(current: Decimal, previous: Decimal | None, history: list[Decimal]):
    absolute = current - previous if previous is not None else None
    pct = (absolute / previous * Decimal(100)) if previous not in (None, 0) else None
    return {
        "absolute_change": absolute,
        "percentage_change": pct,
        "movement": "increase" if pct and pct > 0 else "decrease" if pct and pct < 0 else "unchanged" if pct == 0 else "initial",
        "lowest": min(history + [current]), "highest": max(history + [current]),
        "average": sum(history + [current], Decimal(0)) / Decimal(len(history) + 1),
        "median": Decimal(str(median([float(x) for x in history + [current]]))),
    }

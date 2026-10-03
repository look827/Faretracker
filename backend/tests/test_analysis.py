from decimal import Decimal
from app.services.analysis import analyze

def test_large_drop():
    a=analyze(Decimal("18000"), Decimal("20000"), [])
    assert a["absolute_change"] == Decimal("-2000")
    assert a["percentage_change"] == Decimal("-10.00")

def test_direction():
    assert analyze(Decimal("22000"),Decimal("20000"),[])["movement"]=="increase"

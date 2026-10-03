from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
from ..models import Monitor, FlightPrice, NotificationEvent
from ..providers.mock import MockFlightDataProvider
from ..services.analysis import analyze
from ..notifications.telegram import TelegramNotifier

def event_key(monitor_id, event_type, price_id): return f"{monitor_id}:{event_type}:{price_id}"

def check_monitor(db: Session, monitor: Monitor):
    provider = MockFlightDataProvider()  # replace with a real provider adapter when credentials are available
    quotes = provider.search_flights(monitor.origin, monitor.destination, monitor.departure_date, monitor.return_date, monitor.airline, monitor.stops)
    if not quotes:
        monitor.last_checked_at = datetime.now(timezone.utc); db.commit(); return {"status":"DATA_UNAVAILABLE"}
    quote = min(quotes, key=lambda q: q.price)
    previous = db.query(FlightPrice).filter_by(monitor_id=monitor.id).order_by(FlightPrice.checked_at.desc()).first()
    history = [x.price for x in db.query(FlightPrice).filter_by(monitor_id=monitor.id).all()]
    row = FlightPrice(monitor_id=monitor.id, airline=quote.airline, flight_number=quote.flight_number, stops=quote.stops, departure_time=quote.departure_time, arrival_time=quote.arrival_time, price=quote.price, currency=quote.currency, checked_at=datetime.now(timezone.utc), source=quote.source)
    db.add(row); db.flush(); monitor.last_checked_at = row.checked_at; db.commit()
    a = analyze(quote.price, previous.price if previous else None, history)
    events=[]
    if previous:
        pct = a["percentage_change"] or Decimal(0)
        if pct <= -Decimal(str(monitor.drop_threshold_pct)): events.append("PRICE_DROP")
        if pct <= -Decimal(str(monitor.large_drop_threshold_pct)): events.append("LARGE_PRICE_DROP")
        if pct >= Decimal(str(monitor.increase_threshold_pct)): events.append("PRICE_INCREASE")
    if not history or quote.price < min(history): events.append("NEW_LOWEST")
    if history and quote.price > max(history): events.append("NEW_HIGHEST")
    if monitor.target_price is not None and quote.price <= monitor.target_price and (previous is None or previous.price > monitor.target_price): events.append("TARGET_REACHED")
    for ev in events:
        key=event_key(monitor.id, ev, row.id)
        if db.query(NotificationEvent).filter_by(event_key=key).first(): continue
        body=f"{monitor.origin} → {monitor.destination}\nDeparture: {monitor.departure_date}\nAirline: {quote.airline}\nCurrent: {quote.currency} {quote.price:,.2f}"
        if previous: body += f"\nPrevious: {previous.price:,.2f}\nChange: {a['absolute_change']:,.2f} ({a['percentage_change']:.2f}%)"
        if ev == "TARGET_REACHED": body += f"\nTarget: {monitor.target_price:,.2f}"
        ok, err = TelegramNotifier().send(ev.replace("_", " "), body)
        db.add(NotificationEvent(monitor_id=monitor.id, channel="telegram", event_type=ev, price_id=row.id, event_key=key, status="sent" if ok else "skipped", error=err))
    db.commit()
    return {"status":"OK", "quote":quote, "analysis":a, "events":events}

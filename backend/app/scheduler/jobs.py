from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from ..db import SessionLocal
from ..models import Monitor
from ..services.monitor import check_monitor
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

def run_due():
    now=datetime.now(timezone.utc); db=SessionLocal()
    try:
        for m in db.query(Monitor).filter_by(enabled=True).all():
            if m.last_checked_at is None or (now-m.last_checked_at).total_seconds() >= m.frequency_minutes*60:
                try: check_monitor(db,m)
                except Exception as exc: print(f"monitor {m.id} failed: {exc}")
    finally: db.close()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(run_due, "interval", minutes=1, id="fare-monitor", replace_existing=True)
        scheduler.start()

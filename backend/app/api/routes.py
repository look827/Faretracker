from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Monitor, FlightPrice
from ..schemas.schemas import MonitorCreate, MonitorOut, PriceOut
from ..services.monitor import check_monitor
router=APIRouter(prefix="/api")

@router.get("/health")
def health(): return {"status":"ok"}

@router.post("/monitors", response_model=MonitorOut)
def create_monitor(payload: MonitorCreate, db: Session=Depends(get_db)):
    m=Monitor(**payload.model_dump()); m.origin=m.origin.upper(); m.destination=m.destination.upper(); db.add(m); db.commit(); db.refresh(m); return m

@router.get("/monitors", response_model=list[MonitorOut])
def monitors(db: Session=Depends(get_db)): return db.query(Monitor).order_by(Monitor.id.desc()).all()

@router.get("/monitors/{monitor_id}/prices", response_model=list[PriceOut])
def prices(monitor_id:int, period:str="all", db:Session=Depends(get_db)):
    q=db.query(FlightPrice).filter_by(monitor_id=monitor_id)
    if period != "all":
        days={"24h":1,"7d":7,"30d":30,"90d":90}.get(period)
        if not days: raise HTTPException(400,"period must be 24h, 7d, 30d, 90d or all")
        q=q.filter(FlightPrice.checked_at >= datetime.now(timezone.utc)-timedelta(days=days))
    return q.order_by(FlightPrice.checked_at.asc()).all()

@router.post("/monitors/{monitor_id}/check")
def check(monitor_id:int, db:Session=Depends(get_db)):
    m=db.get(Monitor, monitor_id)
    if not m: raise HTTPException(404,"monitor not found")
    result=check_monitor(db,m); return {"status":result["status"],"events":result.get("events",[])}

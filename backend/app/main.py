from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import Base, engine
from .api.routes import router
from .scheduler.jobs import start_scheduler
from . import models
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Flight Fare Monitor", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
@app.on_event("startup")
def startup(): start_scheduler()

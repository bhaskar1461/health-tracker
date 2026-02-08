from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from app.db import session as db_session
from app.crud import basic
from app.schemas.health_data import HealthDataCreate, HealthDataOut
from app.services.zepp_service import zepp_service
from app.core.config import settings

router = APIRouter()

# NOTE: For simplicity, auth is done via a simple header token that contains user id in `X-User-Id` for demo.
# In production use OAuth/JWT dependency to get current user.

def get_current_user_id(x_user_id: str | None = None):
    # This is a tiny placeholder; callers should pass header `X-User-Id` with user id
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing X-User-Id header for demo auth")
    try:
        return int(x_user_id)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid X-User-Id header")

@router.post("/", response_model=HealthDataOut)
def create_health(health_in: HealthDataCreate, db: Session = Depends(db_session.get_db), x_user_id: str | None = Header(None)):
    user_id = get_current_user_id(x_user_id)
    obj = basic.create_health_data(db, user_id=user_id, obj_in=health_in)
    return obj

@router.get("/", response_model=List[HealthDataOut])
def list_health(db: Session = Depends(db_session.get_db), x_user_id: str | None = Header(None)):
    user_id = get_current_user_id(x_user_id)
    return basic.get_health_for_user(db, user_id)

@router.get("/summary")
def summary(db: Session = Depends(db_session.get_db), x_user_id: str | None = Header(None)):
    user_id = get_current_user_id(x_user_id)
    latest = basic.get_latest_health(db, user_id)
    return {"latest": latest}

@router.post("/sync-zepp")
def sync_zepp(db: Session = Depends(db_session.get_db), x_user_id: str | None = Header(None)):
    """Sync health data from Zepp app"""
    user_id = get_current_user_id(x_user_id)

    # Check if Zepp credentials are configured
    if not settings.ZEPP_PHONE or not settings.ZEPP_PASSWORD:
        raise HTTPException(status_code=400, detail="Zepp credentials not configured. Set ZEPP_PHONE and ZEPP_PASSWORD environment variables.")

    # Login to Zepp
    if not zepp_service.login(settings.ZEPP_PHONE, settings.ZEPP_PASSWORD):
        raise HTTPException(status_code=401, detail="Failed to authenticate with Zepp")

    # Fetch latest data
    zepp_data = zepp_service.get_latest_health_data()
    if not zepp_data:
        raise HTTPException(status_code=404, detail="No health data found in Zepp")

    # Create health entry from Zepp data
    from app.schemas.health_data import HealthDataCreate
    health_create = HealthDataCreate(**zepp_data)
    obj = basic.create_health_data(db, user_id=user_id, obj_in=health_create)

    return {
        "message": "Successfully synced data from Zepp",
        "data": obj,
        "source": "zepp"
    }

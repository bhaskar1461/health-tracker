from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import session as db_session
from app.crud import basic
from app.schemas.health_data import HealthDataCreate, HealthDataOut
from app.services.zepp_service import zepp_service
from app.core.config import settings
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=HealthDataOut)
def create_health(
    health_in: HealthDataCreate,
    db: Session = Depends(db_session.get_db),
    current_user: User = Depends(get_current_user),
):
    obj = basic.create_health_data(db, user_id=current_user.id, obj_in=health_in)
    return obj

@router.get("/", response_model=List[HealthDataOut])
def list_health(
    db: Session = Depends(db_session.get_db),
    current_user: User = Depends(get_current_user),
):
    return basic.get_health_for_user(db, current_user.id)

@router.get("/summary")
def summary(
    db: Session = Depends(db_session.get_db),
    current_user: User = Depends(get_current_user),
):
    latest = basic.get_latest_health(db, current_user.id)
    return {"latest": latest}

@router.post("/sync-zepp")
def sync_zepp(
    db: Session = Depends(db_session.get_db),
    current_user: User = Depends(get_current_user),
):
    """Sync health data from Zepp app"""

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
    obj = basic.create_health_data(db, user_id=current_user.id, obj_in=health_create)

    return {
        "message": "Successfully synced data from Zepp",
        "data": obj,
        "source": "zepp"
    }

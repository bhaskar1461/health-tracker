from fastapi import APIRouter
from app.api.v1.endpoints import auth, health_data

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(health_data.router, tags=["health-data"], prefix="/health-data")

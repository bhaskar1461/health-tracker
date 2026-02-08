from pydantic import BaseModel, conint, confloat
from typing import Optional
from datetime import datetime

class HealthDataBase(BaseModel):
    calories_burned: Optional[confloat(ge=0)] = 0.0
    exercise_minutes: Optional[conint(ge=0)] = 0
    stand_hours: Optional[conint(ge=0, le=24)] = 0
    resting_heart_rate: Optional[conint(ge=0, le=300)] = None
    respiratory_rate: Optional[confloat(ge=0)] = None
    sleep_duration: Optional[confloat(ge=0)] = None
    sleep_quality: Optional[conint(ge=1, le=5)] = None
    sleep_stages: Optional[str] = None

class HealthDataCreate(HealthDataBase):
    pass

class HealthDataOut(HealthDataBase):
    id: int
    user_id: int
    recorded_date: datetime

    class Config:
        orm_mode = True

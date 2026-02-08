from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HealthDataBase(BaseModel):
    calories_burned: Optional[float] = 0.0
    exercise_minutes: Optional[int] = 0
    stand_hours: Optional[int] = 0
    resting_heart_rate: Optional[int] = None
    respiratory_rate: Optional[float] = None
    sleep_duration: Optional[float] = None
    sleep_quality: Optional[int] = None
    sleep_stages: Optional[str] = None

class HealthDataCreate(HealthDataBase):
    pass

class HealthDataOut(HealthDataBase):
    id: int
    user_id: int
    recorded_date: datetime

    class Config:
        orm_mode = True

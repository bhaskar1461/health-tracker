from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class HealthData(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    calories_burned = Column(Float, default=0.0)
    exercise_minutes = Column(Integer, default=0)
    stand_hours = Column(Integer, default=0)

    resting_heart_rate = Column(Integer, nullable=True)
    respiratory_rate = Column(Float, nullable=True)

    sleep_duration = Column(Float, nullable=True)
    sleep_quality = Column(Integer, nullable=True)
    sleep_stages = Column(String, nullable=True)

    recorded_date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

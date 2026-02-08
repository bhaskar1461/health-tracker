from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# User operations

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, email: str, password: str, full_name: str = None):
    hashed = pwd_context.hash(password)
    user = models.User(email=email, hashed_password=hashed, full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Health data

def create_health_data(db: Session, user_id: int, obj_in: schemas.HealthDataCreate):
    obj = models.HealthData(**obj_in.dict(), user_id=user_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_health_for_user(db: Session, user_id: int):
    return db.query(models.HealthData).filter(models.HealthData.user_id == user_id).all()

def get_latest_health(db: Session, user_id: int):
    return db.query(models.HealthData).filter(models.HealthData.user_id == user_id).order_by(models.HealthData.recorded_date.desc()).first()

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import session as db_session
from app.crud import basic
from app.schemas.user import UserOut
from app.core.config import settings
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=Token)
def login(data: LoginIn, db: Session = Depends(db_session.get_db)):
    user = basic.get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not basic.pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user.id), "exp": expire}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/signup", response_model=UserOut)
def signup(data: LoginIn, db: Session = Depends(db_session.get_db)):
    existing = basic.get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="User exists")
    user = basic.create_user(db, data.email, data.password)
    return user

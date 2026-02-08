from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Health Tracker"

    DATABASE_URL: Optional[str] = None

    SECRET_KEY: str = "dev-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Zepp API Configuration
    ZEPP_PHONE: Optional[str] = None
    ZEPP_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()

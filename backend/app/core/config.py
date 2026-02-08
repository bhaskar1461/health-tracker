from pydantic import BaseSettings, Field, validator
from typing import Optional, List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Health Tracker"

    DATABASE_URL: str = "sqlite:///./dev.db"

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ALLOW_ORIGINS: List[str] = []

    # Zepp API Configuration
    ZEPP_PHONE: Optional[str] = None
    ZEPP_PASSWORD: Optional[str] = None

    @validator("CORS_ALLOW_ORIGINS", pre=True)
    def parse_cors_origins(cls, value):
        if value is None:
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    class Config:
        env_file = ".env"

settings = Settings()

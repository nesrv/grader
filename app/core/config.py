import os
from typing import Optional, Dict, Any, List

# Используем Pydantic v2 вместо BaseSettings
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Grader"
    
    # JWT настройки
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "supersecretkey123notforproduction"))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # База данных
    SQLALCHEMY_DATABASE_URI: str = Field(
        default=os.getenv("DATABASE_URL", "sqlite:///./grader.db")
    )
    
    # CORS настройки
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
import os
from pydantic import BaseModel

class Settings(BaseModel):
    """Настройки приложения"""
    PROJECT_NAME: str = "IT-Грейдер"
    PROJECT_DESCRIPTION: str = "Система для подготовки к техническим собеседованиям"
    PROJECT_VERSION: str = "0.1.0"
    
    API_V1_STR: str = "/api/v1"
    
    # Настройки безопасности
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    
    # Настройки базы данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

settings = Settings()
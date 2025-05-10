from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API настройки
    API_V1_STR: str = "/api/v1"
    
    # Настройки безопасности
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # База данных
    DATABASE_URL: str = "sqlite:///./education.db"
    
    # Настройки приложения
    PROJECT_NAME: str = "IT-Грейдер"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "Система для подготовки к техническим собеседованиям"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
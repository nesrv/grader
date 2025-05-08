from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Схема для создания пользователя
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

# Схема для ответа с данными пользователя
class UserResponse(UserBase):
    id: int
    is_active: bool
    xp_points: int
    streak_days: int
    last_activity: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True  # Заменяем orm_mode на from_attributes для Pydantic v2

# Схема для токена доступа
class Token(BaseModel):
    access_token: str
    token_type: str

# Схема для данных токена
class TokenData(BaseModel):
    user_id: Optional[int] = None
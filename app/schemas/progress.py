from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Базовая схема прогресса пользователя
class UserProgressBase(BaseModel):
    user_id: int
    lesson_id: int
    completed: bool = False
    score: float = 0.0
    attempts: int = 0

# Схема для создания записи о прогрессе
class UserProgressCreate(UserProgressBase):
    pass

# Схема для обновления прогресса
class UserProgressUpdate(BaseModel):
    completed: Optional[bool] = None
    score: Optional[float] = None
    attempts: Optional[int] = None

# Схема для ответа с данными о прогрессе
class UserProgressResponse(UserProgressBase):
    id: int
    last_attempt_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Заменяем orm_mode на from_attributes для Pydantic v2

# Схема для списка прогресса
class UserProgressList(BaseModel):
    progress: List[UserProgressResponse]
    total: int
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.lesson import LessonType

# Базовая схема урока
class LessonBase(BaseModel):
    title: str
    description: str
    language_code: str
    level: int
    type: LessonType
    xp_reward: int = 10

# Схема для создания урока
class LessonCreate(LessonBase):
    pass

# Схема для обновления урока
class LessonUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    language_code: Optional[str] = None
    level: Optional[int] = None
    type: Optional[LessonType] = None
    xp_reward: Optional[int] = None
    is_active: Optional[bool] = None

# Схема для ответа с данными урока
class LessonResponse(LessonBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Заменяем orm_mode на from_attributes для Pydantic v2

# Схема для списка уроков
class LessonList(BaseModel):
    lessons: List[LessonResponse]
    total: int
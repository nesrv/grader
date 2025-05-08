from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.exercise import ExerciseType

# Базовая схема упражнения
class ExerciseBase(BaseModel):
    lesson_id: int
    type: ExerciseType
    question: str
    options: Optional[Dict[str, Any]] = None
    correct_answer: str
    hint: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: int = 1

# Схема для создания упражнения
class ExerciseCreate(ExerciseBase):
    pass

# Схема для обновления упражнения
class ExerciseUpdate(BaseModel):
    type: Optional[ExerciseType] = None
    question: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    correct_answer: Optional[str] = None
    hint: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[int] = None
    is_active: Optional[bool] = None

# Схема для ответа с данными упражнения
class ExerciseResponse(ExerciseBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Заменяем orm_mode на from_attributes для Pydantic v2

# Схема для списка упражнений
class ExerciseList(BaseModel):
    exercises: List[ExerciseResponse]
    total: int
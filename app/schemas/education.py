from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Схемы для Grade (Грейд)
class GradeBase(BaseModel):
    name: str
    level: int
    description: Optional[str] = None

class GradeCreate(GradeBase):
    profession_id: int

class GradeUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    description: Optional[str] = None

class Grade(GradeBase):
    grade_id: int
    profession_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# Схемы для Profession (Специальность)
class ProfessionBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProfessionCreate(ProfessionBase):
    pass

class ProfessionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProfessionSimple(ProfessionBase):
    profession_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

class Profession(ProfessionSimple):
    grades: List[Grade] = []

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# Схемы для Module (Модуль)
class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: Optional[int] = 0

class ModuleCreate(ModuleBase):
    profession_id: int
    grade_id: int

class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    profession_id: Optional[int] = None
    grade_id: Optional[int] = None

class Module(ModuleBase):
    module_id: int
    profession_id: int
    grade_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# Схемы для Topic (Тема)
class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = 0

class TopicCreate(TopicBase):
    module_id: int

class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None
    module_id: Optional[int] = None

class Topic(TopicBase):
    topic_id: int
    module_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# Схемы для Question (Вопрос)
class AnswerBase(BaseModel):
    text: str
    is_correct: bool = False
    explanation: Optional[str] = None

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    answer_id: int
    question_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

class QuestionBase(BaseModel):
    text: str
    difficulty: float = 1.0

class QuestionCreate(QuestionBase):
    topic_id: int
    answers: List[AnswerCreate]

class Question(QuestionBase):
    question_id: int
    topic_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    answers: List[Answer] = []

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости
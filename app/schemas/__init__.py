from app.schemas.user import (
    UserBase, UserCreate, UserUpdate, UserResponse,
    Token, TokenData
)
from app.schemas.education import (
    Profession, ProfessionCreate, ProfessionSimple,
    Grade, GradeCreate, GradeUpdate,
    Module, ModuleCreate, ModuleUpdate,
    Topic, TopicCreate, TopicUpdate,
    Question, QuestionCreate,
    Answer, AnswerCreate
)

# Определяем недостающие схемы
from typing import List
from enum import Enum

# ProfessionDetail
class ProfessionDetail(ProfessionSimple):
    """Детальная информация о профессии"""
    grades: List[Grade] = []

    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# GradeDetail
class GradeDetail(Grade):
    """Детальная информация о грейде"""
    
    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# ModuleDetail
class ModuleDetail(Module):
    """Детальная информация о модуле"""
    
    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# TopicDetail
class TopicDetail(Topic):
    """Детальная информация о теме"""
    
    class Config:
        from_attributes = True
        orm_mode = True  # Для обратной совместимости

# QuestionTypeEnum
class QuestionTypeEnum(str, Enum):
    """Перечисление типов вопросов"""
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT = "text"
    CODE = "code"

# Заглушки для остальных схем
class Theory:
    pass

class TheoryCreate:
    pass

class Practice:
    pass

class PracticeCreate:
    pass

class PracticeQuestion:
    pass

class PracticeQuestionCreate:
    pass

class Task:
    pass

class TaskCreate:
    pass

class CaseTask:
    pass

class CaseTaskCreate:
    pass

class Exam:
    pass

class ExamCreate:
    pass

# Импорты из других модулей
from app.schemas.progress import (
    UserProgress, UserProgressCreate,
    UserAnswer, UserAnswerCreate, UserAnswerSubmit, UserAnswerResult,
    TopicProgress, ModuleProgress, GradeProgress, UserStatistics
)
from app.schemas.achievement import (
    Achievement, AchievementCreate,
    UserAchievement, UserAchievementCreate,
    UserRating, UserRatingCreate, UserRatingDetail
)
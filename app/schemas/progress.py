from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime

# Схемы для прогресса пользователя
class UserProgressBase(BaseModel):
    theory_completed: bool = False
    practice_completed: bool = False
    tasks_completed: bool = False
    case_tasks_completed: bool = False
    exam_passed: bool = False
    practice_score: Optional[float] = 0.0
    tasks_score: Optional[float] = 0.0
    case_tasks_score: Optional[float] = 0.0
    exam_score: Optional[float] = 0.0
    time_spent: Optional[int] = 0

class UserProgressCreate(UserProgressBase):
    user_id: int
    topic_id: int

class UserProgress(UserProgressBase):
    user_progress_id: int
    user_id: int
    topic_id: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    last_updated: datetime

    class Config:
        orm_mode = True

# Схемы для ответов пользователя
class UserAnswerBase(BaseModel):
    question_type: str
    question_id: int
    answer: Any
    time_spent: Optional[int] = None
    attempt_number: Optional[int] = 1

class UserAnswerCreate(UserAnswerBase):
    user_id: int

class UserAnswer(UserAnswerBase):
    user_answer_id: int
    user_id: int
    is_correct: Optional[bool] = None
    answered_at: datetime

    class Config:
        orm_mode = True

# Схемы для отправки ответа
class UserAnswerSubmit(BaseModel):
    question_type: str  # practice, task, case_task
    question_id: int
    answer: Any  # Для practice - буква или массив, для task - строка, для case_task - код
    time_spent: Optional[int] = None

# Схемы для результата ответа
class UserAnswerResult(BaseModel):
    is_correct: bool
    correct_answer: Optional[Any] = None
    explanation: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None

# Схемы для статистики пользователя
class TopicProgress(BaseModel):
    topic_id: int
    topic_name: str
    completion_percentage: float
    overall_score: Optional[float] = None
    time_spent: Optional[int] = None
    completed: bool = False

class ModuleProgress(BaseModel):
    module_id: int
    module_name: str
    topics_completed: int
    total_topics: int
    completion_percentage: float
    average_score: Optional[float] = None

class GradeProgress(BaseModel):
    grade_id: int
    grade_name: str
    modules_completed: int
    total_modules: int
    completion_percentage: float
    average_score: Optional[float] = None

class UserStatistics(BaseModel):
    total_topics_completed: int
    total_exams_passed: int
    average_score: Optional[float] = None
    total_time_spent: int  # В секундах
    grade_progress: List[GradeProgress] = []
    recent_activities: List[UserAnswer] = []
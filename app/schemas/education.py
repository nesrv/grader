from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum

# Схемы для профессий
class ProfessionBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None

class ProfessionCreate(ProfessionBase):
    pass

class Profession(ProfessionBase):
    profession_id: int

    class Config:
        orm_mode = True

# Схемы для грейдов
class GradeBase(BaseModel):
    name: str
    description: Optional[str] = None
    level: Optional[int] = None

class GradeCreate(GradeBase):
    profession_id: int

class Grade(GradeBase):
    grade_id: int
    profession_id: int

    class Config:
        orm_mode = True

# Схемы для модулей
class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    order_index: Optional[int] = 0

class ModuleCreate(ModuleBase):
    grade_id: int

class Module(ModuleBase):
    module_id: int
    grade_id: int

    class Config:
        orm_mode = True

# Схемы для тем
class TopicBase(BaseModel):
    name: str
    description: Optional[str] = None
    order_index: Optional[int] = 0

class TopicCreate(TopicBase):
    module_id: int

class Topic(TopicBase):
    topic_id: int
    module_id: int

    class Config:
        orm_mode = True

# Схемы для теории
class TheoryBase(BaseModel):
    content: str

class TheoryCreate(TheoryBase):
    topic_id: int

class Theory(TheoryBase):
    theory_id: int
    topic_id: int

    class Config:
        orm_mode = True

# Перечисление типов вопросов
class QuestionTypeEnum(str, Enum):
    SINGLE_CHOICE = "выбор одного"
    MULTIPLE_CHOICE = "множественный выбор"

# Схемы для вопросов практики
class PracticeQuestionBase(BaseModel):
    question: str
    question_type: QuestionTypeEnum = QuestionTypeEnum.SINGLE_CHOICE
    options: Any  # JSON: {"A": "Вариант 1", "B": "Вариант 2"}
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: Optional[int] = 1

class PracticeQuestionCreate(PracticeQuestionBase):
    practice_id: int

class PracticeQuestion(PracticeQuestionBase):
    practice_question_id: int
    practice_id: int

    class Config:
        orm_mode = True

# Схемы для практики
class PracticeBase(BaseModel):
    pass

class PracticeCreate(PracticeBase):
    topic_id: int

class Practice(PracticeBase):
    practice_id: int
    topic_id: int
    questions: List[PracticeQuestion] = []

    class Config:
        orm_mode = True

# Схемы для задач
class TaskBase(BaseModel):
    question: str
    description: Optional[str] = None
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: Optional[int] = 1

class TaskCreate(TaskBase):
    topic_id: int

class Task(TaskBase):
    task_id: int
    topic_id: int

    class Config:
        orm_mode = True

# Схемы для кейсов
class CaseTaskBase(BaseModel):
    title: str
    description: str
    initial_code: Optional[str] = None
    solution_code: Optional[str] = None
    test_cases: Optional[Any] = None  # JSON с тестовыми случаями
    difficulty: Optional[int] = 1

class CaseTaskCreate(CaseTaskBase):
    topic_id: int

class CaseTask(CaseTaskBase):
    case_task_id: int
    topic_id: int

    class Config:
        orm_mode = True

# Схемы для зачетов
class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    passing_score: Optional[float] = 70.0

class ExamCreate(ExamBase):
    topic_id: int

class Exam(ExamBase):
    exam_id: int
    topic_id: int
    practice_questions: List[PracticeQuestion] = []
    tasks: List[Task] = []
    case_tasks: List[CaseTask] = []

    class Config:
        orm_mode = True

# Детальные схемы с вложенными объектами
class TopicDetail(Topic):
    theory: Optional[Theory] = None
    practice: Optional[Practice] = None
    tasks: List[Task] = []
    case_tasks: List[CaseTask] = []
    exam: Optional[Exam] = None

class ModuleDetail(Module):
    topics: List[Topic] = []

class GradeDetail(Grade):
    modules: List[Module] = []

class ProfessionDetail(Profession):
    grades: List[Grade] = []
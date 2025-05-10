from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, Table, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

# Профессии
class Profession(Base):
    __tablename__ = 'professions'
    profession_id = Column(Integer, primary_key=True) 
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(255))  # Путь к иконке профессии
    grades = relationship("Grade", back_populates="profession")

# Грейды
class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)  
    name = Column(String(50), nullable=False)
    description = Column(Text)
    level = Column(Integer)  # Уровень сложности (1-6)
    profession_id = Column(Integer, ForeignKey('professions.profession_id'))  
    profession = relationship("Profession", back_populates="grades")
    modules = relationship("Module", back_populates="grade")

# Модули
class Module(Base):
    __tablename__ = 'modules'
    module_id = Column(Integer, primary_key=True) 
    name = Column(String(100), nullable=False)
    description = Column(Text)
    order_index = Column(Integer, default=0)  # Для сортировки
    grade_id = Column(Integer, ForeignKey('grades.grade_id'))  
    grade = relationship("Grade", back_populates="modules")
    topics = relationship("Topic", back_populates="module")

# Темы
class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True) 
    name = Column(String(100), nullable=False)
    description = Column(Text)
    order_index = Column(Integer, default=0)  # Для сортировки
    module_id = Column(Integer, ForeignKey('modules.module_id'))  
    module = relationship("Module", back_populates="topics")
    theory = relationship("Theory", uselist=False, back_populates="topic")
    practice = relationship("Practice", uselist=False, back_populates="topic")
    tasks = relationship("Task", back_populates="topic")
    case_tasks = relationship("CaseTask", back_populates="topic")
    exam = relationship("Exam", uselist=False, back_populates="topic")
    user_progress = relationship("UserProgress", back_populates="topic")

# Теория
class Theory(Base):
    __tablename__ = 'theory'
    theory_id = Column(Integer, primary_key=True) 
    content = Column(Text, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="theory")

# Практика (вопросы с выбором ответа)
class Practice(Base):
    __tablename__ = 'practice'
    practice_id = Column(Integer, primary_key=True) 
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="practice")
    questions = relationship("PracticeQuestion", back_populates="practice")

class QuestionType(enum.Enum):
    SINGLE_CHOICE = "выбор одного"
    MULTIPLE_CHOICE = "множественный выбор"

class PracticeQuestion(Base):
    __tablename__ = 'practice_questions'
    practice_question_id = Column(Integer, primary_key=True) 
    question = Column(Text, nullable=False)
    question_type = Column(String(20), default="SINGLE_CHOICE")
    options = Column(Text)  # JSON: {"A": "Вариант 1", "B": "Вариант 2"}
    correct_answer = Column(String(255), nullable=False)  # Для одиночного выбора - буква, для множественного - JSON массив
    explanation = Column(Text)  # Объяснение правильного ответа
    difficulty = Column(Integer, default=1)  # Сложность от 1 до 5
    practice_id = Column(Integer, ForeignKey('practice.practice_id'))  
    practice = relationship("Practice", back_populates="questions")

# Задачи (ввод ответа)
class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True) 
    question = Column(Text, nullable=False)
    description = Column(Text)
    correct_answer = Column(String(100), nullable=False)
    explanation = Column(Text)  # Объяснение решения
    difficulty = Column(Integer, default=1)  # Сложность от 1 до 5
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="tasks")

# Кейсы (написание кода)
class CaseTask(Base):
    __tablename__ = 'case_tasks'
    case_task_id = Column(Integer, primary_key=True) 
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    initial_code = Column(Text)  # Начальный код для задания
    solution_code = Column(Text)  # Эталонное решение
    test_cases = Column(Text)  # JSON с тестовыми случаями
    difficulty = Column(Integer, default=1)  # Сложность от 1 до 5
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="case_tasks")

# Зачет (контрольные вопросы)
class Exam(Base):
    __tablename__ = 'exams'
    exam_id = Column(Integer, primary_key=True) 
    title = Column(String(255), nullable=False)
    description = Column(Text)
    passing_score = Column(Float, default=70.0)  # Проходной балл в процентах
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="exam")

# Связи для зачета
exam_practice_questions = Table('exam_practice_questions', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.exam_id')),
    Column('practice_question_id', Integer, ForeignKey('practice_questions.practice_question_id'))
)

exam_tasks = Table('exam_tasks', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.exam_id')),
    Column('task_id', Integer, ForeignKey('tasks.task_id'))
)

exam_case_tasks = Table('exam_case_tasks', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.exam_id')),
    Column('case_task_id', Integer, ForeignKey('case_tasks.case_task_id'))
)
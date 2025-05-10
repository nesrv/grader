from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

# Прогресс пользователя
class UserProgress(Base):
    __tablename__ = 'user_progress'
    user_progress_id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    
    # Прогресс по теме
    theory_completed = Column(Boolean, default=False)
    practice_completed = Column(Boolean, default=False)
    tasks_completed = Column(Boolean, default=False)
    case_tasks_completed = Column(Boolean, default=False)
    exam_passed = Column(Boolean, default=False)
    
    # Статистика
    practice_score = Column(Float, default=0.0)  # Процент правильных ответов
    tasks_score = Column(Float, default=0.0)  # Процент правильных ответов
    case_tasks_score = Column(Float, default=0.0)  # Процент правильных решений
    exam_score = Column(Float, default=0.0)  # Результат зачета
    
    # Время
    time_spent = Column(Integer, default=0)  # В секундах
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    user = relationship("User", back_populates="progress")
    topic = relationship("Topic", back_populates="user_progress")

# Детальные ответы пользователя
class UserAnswer(Base):
    __tablename__ = 'user_answers'
    user_answer_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    
    # Тип вопроса (practice, task, case_task)
    question_type = Column(String(20), nullable=False)
    
    # ID вопроса (в зависимости от типа)
    question_id = Column(Integer, nullable=False)
    
    # Ответ пользователя
    answer = Column(Text)  # Для practice - буква или массив, для task - строка, для case_task - код
    
    # Результат
    is_correct = Column(Boolean)
    
    # Время
    time_spent = Column(Integer)  # В секундах
    answered_at = Column(DateTime, default=datetime.utcnow)
    
    # Попытки
    attempt_number = Column(Integer, default=1)
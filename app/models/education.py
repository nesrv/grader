from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Profession(Base):
    """Модель профессиональной специальности"""
    __tablename__ = "professions"
    
    profession_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Отношения
    grades = relationship("Grade", back_populates="profession", cascade="all, delete-orphan")
    modules = relationship("Module", back_populates="profession", cascade="all, delete-orphan")

class Grade(Base):
    """Модель грейда (уровня) специальности"""
    __tablename__ = "grades"
    
    grade_id = Column(Integer, primary_key=True, index=True)
    profession_id = Column(Integer, ForeignKey("professions.profession_id"), nullable=False)
    name = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Отношения
    profession = relationship("Profession", back_populates="grades")
    modules = relationship("Module", back_populates="grade")

class Module(Base):
    """Модель учебного модуля"""
    __tablename__ = "modules"
    
    module_id = Column(Integer, primary_key=True, index=True)
    profession_id = Column(Integer, ForeignKey("professions.profession_id"), nullable=False)
    grade_id = Column(Integer, ForeignKey("grades.grade_id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Отношения
    profession = relationship("Profession", back_populates="modules")
    grade = relationship("Grade", back_populates="modules")
    topics = relationship("Topic", back_populates="module", cascade="all, delete-orphan")

class Topic(Base):
    """Модель темы в учебном модуле"""
    __tablename__ = "topics"
    
    topic_id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.module_id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Отношения
    module = relationship("Module", back_populates="topics")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")

class Question(Base):
    """Модель вопроса для проверки знаний"""
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.topic_id"), nullable=False)
    text = Column(Text, nullable=False)
    difficulty = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Отношения
    topic = relationship("Topic", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

class Answer(Base):
    """Модель варианта ответа на вопрос"""
    __tablename__ = "answers"
    
    answer_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Отношения
    question = relationship("Question", back_populates="answers")
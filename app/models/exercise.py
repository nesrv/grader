from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class ExerciseType(str, enum.Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    FILL_BLANK = "fill_blank"
    MATCH_PAIRS = "match_pairs"
    ARRANGE_WORDS = "arrange_words"
    TRANSLATION = "translation"
    LISTENING = "listening"
    SPEAKING = "speaking"

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    type = Column(Enum(ExerciseType))
    question = Column(Text)
    options = Column(JSON, nullable=True)  # Для вариантов ответа
    correct_answer = Column(Text)
    hint = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Integer, default=1)  # От 1 до 5
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Отношения
    lesson = relationship("Lesson", back_populates="exercises")

# Добавляем отношение в модель Lesson
from app.models.lesson import Lesson
Lesson.exercises = relationship("Exercise", back_populates="lesson")
from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class LessonType(str, enum.Enum):
    VOCABULARY = "vocabulary"
    GRAMMAR = "grammar"
    LISTENING = "listening"
    SPEAKING = "speaking"
    READING = "reading"
    WRITING = "writing"

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    language_code = Column(String(2))  # ISO 639-1 код языка (en, es, fr, etc.)
    level = Column(Integer)  # Уровень сложности
    type = Column(Enum(LessonType))
    xp_reward = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
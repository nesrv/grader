from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

# Достижения пользователя
class Achievement(Base):
    __tablename__ = 'achievements'
    achievement_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(255))  # Путь к иконке достижения
    criteria = Column(Text)  # JSON с критериями получения

class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    user_achievement_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.achievement_id'), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")

# Рейтинг пользователей
class UserRating(Base):
    __tablename__ = 'user_ratings'
    user_rating_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    profession_id = Column(Integer, ForeignKey('professions.profession_id'), nullable=False)
    rating_score = Column(Integer, default=0)
    topics_completed = Column(Integer, default=0)
    exams_passed = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Отношения
    user = relationship("User")
    profession = relationship("Profession")
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Схемы для достижений
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    criteria: Optional[str] = None  # JSON с критериями получения

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    achievement_id: int

    class Config:
        orm_mode = True

# Схемы для достижений пользователя
class UserAchievementBase(BaseModel):
    user_id: int
    achievement_id: int

class UserAchievementCreate(UserAchievementBase):
    pass

class UserAchievement(UserAchievementBase):
    user_achievement_id: int
    earned_at: datetime
    achievement: Achievement

    class Config:
        orm_mode = True

# Схемы для рейтинга пользователей
class UserRatingBase(BaseModel):
    user_id: int
    profession_id: int
    rating_score: int = 0
    topics_completed: int = 0
    exams_passed: int = 0

class UserRatingCreate(UserRatingBase):
    pass

class UserRating(UserRatingBase):
    user_rating_id: int
    last_updated: datetime
    username: Optional[str] = None  # Добавляем для отображения в рейтинге

    class Config:
        orm_mode = True

# Детальная схема рейтинга пользователя
class UserRatingDetail(UserRating):
    profession_name: str
    rank: int  # Позиция в рейтинге
    total_users: int  # Общее количество пользователей в рейтинге
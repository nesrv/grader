from app.models.user import User
from app.models.education import (
    Profession, Grade, Module, Topic, Theory, 
    Practice, PracticeQuestion, QuestionType,
    Task, CaseTask, Exam
)
from app.models.progress import UserProgress, UserAnswer
from app.models.achievement import Achievement, UserAchievement, UserRating

# Для удобства импорта всех моделей
__all__ = [
    'User',
    'Profession', 'Grade', 'Module', 'Topic', 'Theory',
    'Practice', 'PracticeQuestion', 'QuestionType',
    'Task', 'CaseTask', 'Exam',
    'UserProgress', 'UserAnswer',
    'Achievement', 'UserAchievement', 'UserRating'
]
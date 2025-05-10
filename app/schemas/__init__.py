from app.schemas.user import (
    UserBase, UserCreate, UserUpdate, UserResponse,
    Token, TokenData
)
from app.schemas.education import (
    Profession, ProfessionCreate, ProfessionDetail,
    Grade, GradeCreate, GradeDetail,
    Module, ModuleCreate, ModuleDetail,
    Topic, TopicCreate, TopicDetail,
    Theory, TheoryCreate,
    Practice, PracticeCreate,
    PracticeQuestion, PracticeQuestionCreate,
    Task, TaskCreate,
    CaseTask, CaseTaskCreate,
    Exam, ExamCreate,
    QuestionTypeEnum
)
from app.schemas.progress import (
    UserProgress, UserProgressCreate,
    UserAnswer, UserAnswerCreate, UserAnswerSubmit, UserAnswerResult,
    TopicProgress, ModuleProgress, GradeProgress, UserStatistics
)
from app.schemas.achievement import (
    Achievement, AchievementCreate,
    UserAchievement, UserAchievementCreate,
    UserRating, UserRatingCreate, UserRatingDetail
)
from fastapi import APIRouter

from app.api.v1.endpoints import auth, professions, grades
from app.api.v1 import user

api_router = APIRouter()

# Подключаем существующие эндпоинты
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(professions.router, prefix="/professions", tags=["Professions"])
api_router.include_router(grades.router, prefix="/grades", tags=["Grades"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])

# Добавьте остальные маршруты по мере создания соответствующих файлов
# api_router.include_router(modules.router, prefix="/modules", tags=["Modules"])
# api_router.include_router(topics.router, prefix="/topics", tags=["Topics"])
# api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])
# api_router.include_router(ratings.router, prefix="/ratings", tags=["Ratings"])
# api_router.include_router(achievements.router, prefix="/achievements", tags=["Achievements"])
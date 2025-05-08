from fastapi import FastAPI
from app.api.v1 import user, lesson, progress
from app.core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Grader API",
    description="API для аналога Duolingo с поддержкой мобильного и веб-клиента",
    version="0.1.0"
)

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры API
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(lesson.router, prefix="/api/v1/lessons", tags=["Lessons"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Grader API - аналог Duolingo"}
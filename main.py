from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, engine

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Определяем базовый путь проекта
BASE_PATH = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)

# Настройка CORS для работы с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Проверяем существование директорий
static_dir = BASE_PATH / "app" / "static"
templates_dir = BASE_PATH / "app" / "templates"

if not static_dir.exists():
    os.makedirs(static_dir)
    print(f"Created static directory: {static_dir}")

if not templates_dir.exists():
    os.makedirs(templates_dir)
    print(f"Created templates directory: {templates_dir}")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory=str(templates_dir))

# Подключаем API маршруты
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Отображение главной страницы"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Отображение страницы входа"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Отображение страницы регистрации"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/lessons", response_class=HTMLResponse)
async def lessons_page(request: Request):
    """Отображение страницы уроков"""
    return templates.TemplateResponse("lessons.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    """Отображение страницы профиля пользователя"""
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/ratings", response_class=HTMLResponse)
async def ratings_page(request: Request):
    """Отображение страницы рейтингов"""
    return templates.TemplateResponse("ratings.html", {"request": request})

@app.get("/achievements", response_class=HTMLResponse)
async def achievements_page(request: Request):
    """Отображение страницы достижений"""
    return templates.TemplateResponse("achievements.html", {"request": request})

# Маршруты для админки
@app.get("/admin", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Отображение страницы входа в админку"""
    return templates.TemplateResponse("admin/login.html", {"request": request})

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard_page(request: Request):
    """Отображение главной страницы админки"""
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    """Обработка запроса favicon.ico"""
    return RedirectResponse(url="/static/images/favicon.ico")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
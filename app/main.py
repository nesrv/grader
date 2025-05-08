from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

from app.api.v1 import user, lesson, progress, auth
from app.core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Определяем базовый путь проекта
BASE_PATH = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="IT-Грейдер API",
    description="API для системы подготовки к техническим собеседованиям",
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

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "static")), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# Подключаем роутеры API
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(lesson.router, prefix="/api/v1/lessons", tags=["Lessons"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["Progress"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Отображение главной страницы в стиле Duolingo"""
    return templates.TemplateResponse("duolingo-style.html", {"request": request})

@app.get("/lessons", response_class=HTMLResponse)
async def lessons_page(request: Request):
    """Отображение страницы уроков"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Уроки | IT-Грейдер</title>
        <link rel="stylesheet" href="/static/css/duolingo-style.css">
        <style>
            .lessons-container {
                padding: 120px 0 60px;
            }
            
            .lessons-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
            }
            
            .lessons-title {
                font-size: 32px;
                color: var(--text-color);
            }
            
            .lessons-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 30px;
            }
            
            .lesson-card {
                background-color: var(--background-color);
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 4px 12px var(--shadow-color);
                transition: transform 0.3s, box-shadow 0.3s;
            }
            
            .lesson-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 24px var(--shadow-color);
            }
            
            .lesson-card__image {
                height: 160px;
                background-color: var(--light-gray);
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .lesson-card__image img {
                max-width: 80px;
                height: auto;
            }
            
            .lesson-card__content {
                padding: 20px;
            }
            
            .lesson-card__title {
                font-size: 20px;
                margin-bottom: 10px;
                color: var(--text-color);
            }
            
            .lesson-card__type {
                color: var(--text-light);
                text-transform: uppercase;
                font-size: 14px;
                margin-bottom: 15px;
            }
            
            .lesson-card__description {
                font-size: 14px;
                color: var(--text-light);
                margin-bottom: 20px;
            }
            
            .lesson-card__footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .lesson-card__xp {
                font-size: 14px;
                font-weight: 600;
                color: var(--primary-color);
            }
            
            .user-info {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            
            .user-greeting {
                font-weight: 600;
            }
            
            .back-btn {
                margin-right: 15px;
                color: var(--text-color);
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .back-btn:hover {
                color: var(--primary-color);
            }
            
            .no-auth {
                text-align: center;
                padding: 60px 20px;
                background-color: var(--light-gray);
                border-radius: 16px;
                margin: 60px 0;
            }
            
            .no-auth h2 {
                font-size: 28px;
                margin-bottom: 20px;
                color: var(--text-color);
            }
            
            .no-auth p {
                font-size: 16px;
                color: var(--text-light);
                margin-bottom: 30px;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
    </head>
    <body>
        <header class="header">
            <div class="container header__container">
                <div class="header__logo">
                    <a href="/">
                        <img src="/static/images/logo-black.svg" alt="IT-Грейдер" class="logo">
                    </a>
                </div>
                <nav class="header__nav">
                    <ul class="nav-list">
                        <li><a href="/" class="nav-link">ГРЕЙДЫ</a></li>
                        <li><a href="#" class="nav-link">О НАС</a></li>
                        <li><a href="#" class="nav-link">МЕТОДИКА</a></li>
                        <li><a href="#" class="nav-link">ПРОГРЕСС</a></li>
                    </ul>
                </nav>
                <div class="header__auth" id="headerAuth">
                    <button class="btn btn--secondary" id="loginBtn">ВОЙТИ</button>
                    <button class="btn btn--primary" id="registerBtn">НАЧАТЬ</button>
                </div>
            </div>
        </header>

        <div class="lessons-container container">
            <div class="lessons-header">
                <h1 class="lessons-title" id="categoryTitle">Уроки</h1>
                <div class="user-info" id="userInfo" style="display: none;">
                    <span class="user-greeting" id="username"></span>
                    <button class="btn btn--secondary" id="logoutBtn">Выйти</button>
                </div>
            </div>
            
            <div id="lessonsContent">
                <!-- Здесь будут отображаться уроки -->
                <div class="no-auth" id="noAuth">
                    <h2>Для доступа к урокам необходимо авторизоваться</h2>
                    <p>Пожалуйста, вернитесь на главную страницу и войдите в систему или зарегистрируйтесь.</p>
                    <a href="/" class="btn btn--primary">На главную</a>
                </div>
            </div>
        </div>

        <footer class="footer">
            <div class="container">
                <div class="footer__grid">
                    <div class="footer__logo">
                        <img src="/static/images/logo-black.svg" alt="IT-Грейдер" class="logo">
                        <p>Подготовка к техническим собеседованиям</p>
                    </div>
                    <div class="footer__links">
                        <h4>О нас</h4>
                        <ul>
                            <li><a href="#">Грейды</a></li>
                            <li><a href="#">Миссия</a></li>
                            <li><a href="#">Методика</a></li>
                            <li><a href="#">Команда</a></li>
                        </ul>
                    </div>
                    <div class="footer__links">
                        <h4>Продукты</h4>
                        <ul>
                            <li><a href="#">IT-Грейдер Basic</a></li>
                            <li><a href="#">IT-Грейдер Premium</a></li>
                            <li><a href="#">IT-Грейдер для компаний</a></li>
                            <li><a href="#">Тесты IT-Грейдер</a></li>
                        </ul>
                    </div>
                    <div class="footer__links">
                        <h4>Помощь</h4>
                        <ul>
                            <li><a href="#">FAQ</a></li>
                            <li><a href="#">Сообщество</a></li>
                            <li><a href="#">Правила</a></li>
                        </ul>
                    </div>
                </div>
                <div class="footer__bottom">
                    <div class="footer__social">
                        <a href="#" class="social-link"><img src="/static/images/social/facebook.svg" alt="Facebook"></a>
                        <a href="#" class="social-link"><img src="/static/images/social/twitter.svg" alt="Twitter"></a>
                        <a href="#" class="social-link"><img src="/static/images/social/instagram.svg" alt="Instagram"></a>
                    </div>
                    <div class="footer__copyright">
                        <p>&copy; 2025 IT-Грейдер. Все права защищены.</p>
                    </div>
                </div>
            </div>
        </footer>

        <script>
            // Проверяем авторизацию
            const token = localStorage.getItem('token');
            const noAuthBlock = document.getElementById('noAuth');
            const lessonsContent = document.getElementById('lessonsContent');
            const userInfo = document.getElementById('userInfo');
            const headerAuth = document.getElementById('headerAuth');
            const usernameElement = document.getElementById('username');
            
            // Получаем параметры из URL
            const urlParams = new URLSearchParams(window.location.search);
            const grade = urlParams.get('grade');
            const category = urlParams.get('category');
            
            // Обновляем заголовок
            if (category && grade) {
                document.getElementById('categoryTitle').textContent = `${category} - ${grade}`;
                document.title = `${category} - ${grade} | IT-Грейдер`;
            }
            
            // Функция для получения данных пользователя
            async function getUserInfo() {
                try {
                    const response = await fetch('/api/v1/users/me', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    if (response.ok) {
                        const userData = await response.json();
                        usernameElement.textContent = `Привет, ${userData.username}!`;
                        return userData;
                    } else {
                        throw new Error('Не удалось получить данные пользователя');
                    }
                } catch (error) {
                    console.error('Ошибка:', error);
                    localStorage.removeItem('token');
                    showNoAuth();
                }
            }
            
            // Функция для отображения уроков
            function showLessons() {
                noAuthBlock.style.display = 'none';
                userInfo.style.display = 'flex';
                headerAuth.style.display = 'none';
                
                // Примеры уроков в зависимости от выбранного грейда и категории
                let lessonsHTML = '<div class="lessons-grid">';
                
                if (category && category.includes('Python-бэкендеры')) {
                    if (grade === 'стажер') {
                        lessonsHTML += `
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-backend.svg" alt="Backend">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">Основы Python</h2>
                                    <div class="lesson-card__type">Стажер</div>
                                    <p class="lesson-card__description">Изучение базового синтаксиса Python, типов данных, условий и циклов.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 100</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-backend.svg" alt="Backend">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">Структуры данных</h2>
                                    <div class="lesson-card__type">Стажер</div>
                                    <p class="lesson-card__description">Списки, словари, кортежи и множества в Python.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 120</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                        `;
                    } else if (grade === 'джун') {
                        lessonsHTML += `
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-backend.svg" alt="Backend">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">ООП в Python</h2>
                                    <div class="lesson-card__type">Джун</div>
                                    <p class="lesson-card__description">Классы, объекты, наследование, инкапсуляция и полиморфизм.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 150</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-backend.svg" alt="Backend">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">Работа с файлами и исключениями</h2>
                                    <div class="lesson-card__type">Джун</div>
                                    <p class="lesson-card__description">Чтение и запись файлов, обработка исключений.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 130</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                } else if (category && category.includes('Python-аналитики')) {
                    if (grade === 'стажер') {
                        lessonsHTML += `
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-analytics.svg" alt="Analytics">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">Основы NumPy</h2>
                                    <div class="lesson-card__type">Стажер</div>
                                    <p class="lesson-card__description">Работа с массивами NumPy, векторизация операций.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 110</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-analytics.svg" alt="Analytics">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">Основы Pandas</h2>
                                    <div class="lesson-card__type">Стажер</div>
                                    <p class="lesson-card__description">Работа с DataFrame и Series, загрузка и обработка данных.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 120</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                } else if (category && category.includes('Базы данных')) {
                    if (grade === 'стажер') {
                        lessonsHTML += `
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-database.svg" alt="Database">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">Основы SQL</h2>
                                    <div class="lesson-card__type">Стажер</div>
                                    <p class="lesson-card__description">Базовые запросы SELECT, INSERT, UPDATE, DELETE.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 100</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                            <div class="lesson-card">
                                <div class="lesson-card__image">
                                    <img src="/static/images/category-database.svg" alt="Database">
                                </div>
                                <div class="lesson-card__content">
                                    <h2 class="lesson-card__title">Связи между таблицами</h2>
                                    <div class="lesson-card__type">Стажер</div>
                                    <p class="lesson-card__description">Работа с JOIN, внешние ключи, типы связей.</p>
                                    <div class="lesson-card__footer">
                                        <span class="lesson-card__xp">XP: 120</span>
                                        <button class="btn btn--primary lesson-btn">Начать</button>
                                    </div>
                                </div>
                            </div>
                        `;
                    }
                } else {
                    lessonsHTML += `
                        <div class="lesson-card">
                            <div class="lesson-card__image">
                                <img src="/static/images/category-backend.svg" alt="Lesson">
                            </div>
                            <div class="lesson-card__content">
                                <h2 class="lesson-card__title">Урок 1</h2>
                                <div class="lesson-card__type">${grade || 'Базовый'}</div>
                                <p class="lesson-card__description">Описание урока будет добавлено позже.</p>
                                <div class="lesson-card__footer">
                                    <span class="lesson-card__xp">XP: 100</span>
                                    <button class="btn btn--primary lesson-btn">Начать</button>
                                </div>
                            </div>
                        </div>
                        <div class="lesson-card">
                            <div class="lesson-card__image">
                                <img src="/static/images/category-backend.svg" alt="Lesson">
                            </div>
                            <div class="lesson-card__content">
                                <h2 class="lesson-card__title">Урок 2</h2>
                                <div class="lesson-card__type">${grade || 'Базовый'}</div>
                                <p class="lesson-card__description">Описание урока будет добавлено позже.</p>
                                <div class="lesson-card__footer">
                                    <span class="lesson-card__xp">XP: 120</span>
                                    <button class="btn btn--primary lesson-btn">Начать</button>
                                </div>
                            </div>
                        </div>
                    `;
                }
                
                lessonsHTML += '</div>';
                lessonsContent.innerHTML = lessonsHTML;
                
                // Добавляем обработчики для кнопок уроков
                document.querySelectorAll('.lesson-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const lessonTitle = this.closest('.lesson-card__content').querySelector('.lesson-card__title').textContent;
                        alert(`Урок "${lessonTitle}" будет доступен в ближайшее время!`);
                    });
                });
            }
            
            // Функция для отображения блока "не авторизован"
            function showNoAuth() {
                noAuthBlock.style.display = 'block';
                userInfo.style.display = 'none';
            }
            
            // Проверяем авторизацию и отображаем соответствующий контент
            if (token) {
                getUserInfo().then(() => {
                    showLessons();
                });
            } else {
                showNoAuth();
            }
            
            // Обработчик для кнопки выхода
            document.getElementById('logoutBtn').addEventListener('click', function() {
                localStorage.removeItem('token');
                window.location.href = '/';
            });
            
            // Обработчики для кнопок в шапке
            document.getElementById('loginBtn')?.addEventListener('click', function() {
                window.location.href = '/#auth';
            });
            
            document.getElementById('registerBtn')?.addEventListener('click', function() {
                window.location.href = '/#auth';
            });
        </script>
    </body>
    </html>
    """, status_code=200)

# Для обратной совместимости оставляем старые маршруты, но перенаправляем на новые
@app.get("/l", response_class=HTMLResponse)
async def old_landing_page(request: Request):
    """Перенаправление со старой главной страницы на новую"""
    return HTMLResponse(content="""
    <html>
        <head>
            <meta http-equiv="refresh" content="0;url=/" />
        </head>
        <body>
            <p>Перенаправление на <a href="/">главную страницу</a>...</p>
        </body>
    </html>
    """, status_code=200)

@app.get("/l/lessons", response_class=HTMLResponse)
async def old_lessons_page(request: Request):
    """Перенаправление со старой страницы уроков на новую"""
    return HTMLResponse(content="""
    <html>
        <head>
            <meta http-equiv="refresh" content="0;url=/lessons" />
        </head>
        <body>
            <p>Перенаправление на <a href="/lessons">страницу уроков</a>...</p>
        </body>
    </html>
    """, status_code=200)
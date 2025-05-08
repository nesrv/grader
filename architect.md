

Отлично! Вот базовая структура проекта на **FastAPI**, подходящая для аналога Duolingo с мобильным (Kivy) и веб-клиентом (JavaScript):

---

### 📁 Структура проекта

```
grader/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # точка входа в приложение FastAPI
│   ├── models/               # SQLAlchemy модели (User, Lesson, Progress и т.д.)
│   │   └── user.py
│   ├── schemas/              # Pydantic схемы для сериализации
│   │   └── user.py
│   ├── api/                  # маршруты API
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── user.py
│   ├── services/             # логика (например, аутентификация, scoring и т.д.)
│   │   └── auth.py
│   ├── core/                 # конфигурации (настройки, база данных и т.д.)
│   │   ├── config.py
│   │   └── database.py
│   └── deps/                 # зависимости для маршрутов (current_user и др.)
│       └── auth.py
│
├── alembic/                  # миграции базы данных
│
├── requirements.txt
└── run.py                    # запускает сервер
```

---

### 🧠 Что входит в MVP (минимально жизнеспособную версию):

* Регистрация/логин (JWT-токены).
* Получение и обновление прогресса пользователя.
* CRUD для уроков, заданий.
* Простой scoring/XP-механизм.
* Маршруты API, к которым можно обращаться из Kivy и JS.

---

### 🚀 Пример: `main.py`

```python
from fastapi import FastAPI
from app.api.v1 import user
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Duolingo Clone API")

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
```

---

### 🔐 Пример: авторизация (JWT) `auth.py`

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

### 📱 Подключение фронтенда:

* Kivy будет обращаться к API через `requests` или `httpx`.
* JS (vanilla) — через `fetch()` к `https://yourserver.com/api/v1/...`.




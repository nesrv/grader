# Grader - аналог Duolingo на FastAPI

Проект представляет собой API для приложения по изучению языков, аналогичного Duolingo, с поддержкой мобильного (Kivy) и веб-клиента (JavaScript).

## Структура проекта

```
grader/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # точка входа в приложение FastAPI
│   ├── models/               # SQLAlchemy модели (User, Lesson, Progress и т.д.)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── lesson.py
│   │   ├── exercise.py
│   │   └── progress.py
│   ├── schemas/              # Pydantic схемы для сериализации
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── lesson.py
│   │   ├── exercise.py
│   │   └── progress.py
│   ├── api/                  # маршруты API
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── user.py
│   │       ├── lesson.py
│   │       └── progress.py
│   ├── services/             # логика (например, аутентификация, scoring и т.д.)
│   │   ├── auth.py
│   │   └── user.py
│   ├── core/                 # конфигурации (настройки, база данных и т.д.)
│   │   ├── config.py
│   │   └── database.py
│   └── deps/                 # зависимости для маршрутов (current_user и др.)
│       ├── __init__.py
│       └── auth.py
│
├── alembic/                  # миграции базы данных
│
├── requirements.txt
└── run.py                    # запускает сервер
```

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd grader
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте миграции базы данных:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

5. Запустите сервер:
```bash
python run.py
```

Сервер будет доступен по адресу: http://localhost:8000

## API документация

После запуска сервера, документация API будет доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Основные функции

- Регистрация и авторизация пользователей (JWT-токены)
- Управление уроками и упражнениями
- Отслеживание прогресса пользователя
- Система начисления XP и достижений

## Подключение клиентов

### Веб-клиент (JavaScript)
```javascript
// Пример запроса к API
fetch('http://localhost:8000/api/v1/users/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    'username': 'user',
    'password': 'password'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Мобильный клиент (Kivy)
```python
import requests

# Пример запроса к API
response = requests.post(
    'http://localhost:8000/api/v1/users/login',
    data={'username': 'user', 'password': 'password'}
)
data = response.json()
print(data)
```
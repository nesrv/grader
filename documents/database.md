# Проектирование базы данных

## Профессия

* ид_профессии первичный уникальный ключ автоинкремент
* название
* описание_грейда


## Грейды
* ид_грейда первичный уникальный ключ автоинкремент
* ид_профессии (связь многие-к-одному)
* описание грейда

## Модули
* ид_модуля первичный уникальный ключ автоинкремент
* ид_грейда(связь многие-к-одному)
* описание модуля текст дефолт нул

## Темы
* ид_темы первичный уникальный ключ автоинкремент
* ид_модуля(связь многие-к-многим)
* описание темы текст дефолт нул

## Поддтемы
* ид_темы первичный уникальный ключ автоинкремент
* ид_темы(связь многие-к-многим)
* описание темы текст дефолт нул
* тип подтемы (теория, практика, задачи, кейсы, зачет)


## Вопросы для теории

* ид_вопроса
* ид_подтемы(связь подумать)
* название вопроса
* описание вопроса
* варианты ответов (3 варианты, тип массив)
* номер правильного варианта тип int


## Вопросы для практики

* ид_вопроса
* ид_подтемы(связь подумать)
* название вопроса
* варианты ответов (3 варианта, тип массив)
* номера правильных варианта (тип массив)


## Вопросы для практики

* ид_вопроса
* ид_подтемы(связь подумать)
* название вопроса
* опсисание вопросы
* код вопроса 
* правильный ответ (float)


Если вам нужно использовать `NATURAL JOIN` в SQLite, важно, чтобы **совпадали имена столбцов**, по которым происходит соединение.  

### **Изменения в моделях:**
1. **Заменим `id` на `[table_name]_id`** (например, `profession_id`, `grade_id`).  
2. **Внешние ключи должны называться так же, как первичные** (чтобы `NATURAL JOIN` работал автоматически).  

---

## **Обновленный код SQLAlchemy**  

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Профессии
class Profession(Base):
    __tablename__ = 'professions'
    profession_id = Column(Integer, primary_key=True) 
    name = Column(String(100), nullable=False)
    description = Column(Text)
    grades = relationship("Grade", back_populates="profession")

# Грейды
class Grade(Base):
    __tablename__ = 'grades'
    grade_id = Column(Integer, primary_key=True)  
    name = Column(String(50), nullable=False)
    profession_id = Column(Integer, ForeignKey('professions.profession_id'))  
    profession = relationship("Profession", back_populates="grades")
    modules = relationship("Module", back_populates="grade")

# Модули
class Module(Base):
    __tablename__ = 'modules'
    module_id = Column(Integer, primary_key=True) 
    name = Column(String(100), nullable=False)
    grade_id = Column(Integer, ForeignKey('grades.grade_id'))  
    grade = relationship("Grade", back_populates="modules")
    topics = relationship("Topic", back_populates="module")

# Темы
class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True) 
    name = Column(String(100), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.module_id'))  
    module = relationship("Module", back_populates="topics")
    theory = relationship("Theory", uselist=False, back_populates="topic")
    practice = relationship("Practice", uselist=False, back_populates="topic")
    tasks = relationship("Task", back_populates="topic")
    case_tasks = relationship("CaseTask", back_populates="topic")
    exam = relationship("Exam", uselist=False, back_populates="topic")
    user_progress = relationship("UserProgress", back_populates="topic")

# Теория
class Theory(Base):
    __tablename__ = 'theory'
    theory_id = Column(Integer, primary_key=True) 
    content = Column(Text, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="theory")

# Практика (вопросы с выбором ответа)
class Practice(Base):
    __tablename__ = 'practice'
    practice_id = Column(Integer, primary_key=True) 
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="practice")
    questions = relationship("PracticeQuestion", back_populates="practice")

class PracticeQuestion(Base):
    __tablename__ = 'practice_questions'
    practice_question_id = Column(Integer, primary_key=True) 
    question = Column(Text, nullable=False)
    options = Column(Text)  # JSON: {"A": "Вариант 1", "B": "Вариант 2"}
    correct_answer = Column(String(10), nullable=False)
    practice_id = Column(Integer, ForeignKey('practice.practice_id'))  
    practice = relationship("Practice", back_populates="questions")

# Задачи (ввод ответа)
class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True) 
    question = Column(Text, nullable=False)
    correct_answer = Column(String(100), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="tasks")

# Кейсы (написание кода)
class CaseTask(Base):
    __tablename__ = 'case_tasks'
    case_task_id = Column(Integer, primary_key=True) 
    description = Column(Text, nullable=False)
    solution_code = Column(Text)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="case_tasks")

# Зачет (контрольные вопросы)
class Exam(Base):
    __tablename__ = 'exams'
    exam_id = Column(Integer, primary_key=True) 
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="exam")
    practice_questions = relationship("PracticeQuestion", secondary="exam_practice_questions")
    tasks = relationship("Task", secondary="exam_tasks")
    case_tasks = relationship("CaseTask", secondary="exam_case_tasks")

# Таблицы связи (многие-ко-многим)
exam_practice_questions = Table('exam_practice_questions', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.exam_id')),
    Column('practice_question_id', Integer, ForeignKey('practice_questions.practice_question_id'))
)

exam_tasks = Table('exam_tasks', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.exam_id')),
    Column('task_id', Integer, ForeignKey('tasks.task_id'))
)

exam_case_tasks = Table('exam_case_tasks', Base.metadata,
    Column('exam_id', Integer, ForeignKey('exams.exam_id')),
    Column('case_task_id', Integer, ForeignKey('case_tasks.case_task_id'))
)

# Прогресс пользователя
class UserProgress(Base):
    __tablename__ = 'user_progress'
    user_progress_id = Column(Integer, primary_key=True) 
    user_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))  
    topic = relationship("Topic", back_populates="user_progress")
    theory_completed = Column(Boolean, default=False)
    practice_score = Column(Float)
    tasks_score = Column(Float)
    case_tasks_score = Column(Float)
    exam_passed = Column(Boolean, default=False)
    time_spent = Column(Integer)  # В секундах
    last_updated = Column(DateTime, default=datetime.utcnow)

# Создание БД
engine = create_engine('sqlite:///education.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
```

---

### **Пример использования `NATURAL JOIN`**  
Теперь можно делать запросы вроде:  

```sql
-- Получить все темы модуля с автоматическим соединением по `module_id`
SELECT * FROM modules NATURAL JOIN topics;

-- Получить все вопросы практики по теме (соединение по `topic_id`)
SELECT * FROM topics NATURAL JOIN practice NATURAL JOIN practice_questions;
```

### **Плюсы и минусы**  
✅ **Плюсы:**  
- `NATURAL JOIN` работает без явного указания `ON`.  
- Удобно для простых связей.  

❌ **Минусы:**  
- Опасно, если в таблицах есть другие совпадающие столбцы (может соединить неожиданно).  
- Лучше использовать `JOIN ... ON` для сложных запросов.  

---

### **Вывод**  
Теперь структура БД позволяет использовать `NATURAL JOIN`, но **лучше применять его осторожно**. Для надежности можно продолжать использовать явные `JOIN ... ON`.
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.user import User
from app.models.lesson import Lesson, LessonType
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse, LessonList
from app.services.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
def create_lesson(
    lesson_create: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создание нового урока"""
    db_lesson = Lesson(**lesson_create.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.get("/", response_model=LessonList)
def read_lessons(
    skip: int = 0,
    limit: int = 100,
    language: Optional[str] = None,
    level: Optional[int] = None,
    type: Optional[LessonType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение списка уроков с фильтрацией"""
    query = db.query(Lesson)
    
    # Применяем фильтры
    if language:
        query = query.filter(Lesson.language_code == language)
    if level:
        query = query.filter(Lesson.level == level)
    if type:
        query = query.filter(Lesson.type == type)
    
    # Получаем общее количество
    total = query.count()
    
    # Применяем пагинацию
    lessons = query.offset(skip).limit(limit).all()
    
    return {"lessons": lessons, "total": total}

@router.get("/{lesson_id}", response_model=LessonResponse)
def read_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение урока по ID"""
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Урок с ID {lesson_id} не найден"
        )
    return db_lesson

@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson_update: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновление урока"""
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Урок с ID {lesson_id} не найден"
        )
    
    # Обновляем поля урока
    update_data = lesson_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lesson, key, value)
    
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.delete("/{lesson_id}", response_model=LessonResponse)
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаление урока"""
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Урок с ID {lesson_id} не найден"
        )
    
    db.delete(db_lesson)
    db.commit()
    return db_lesson
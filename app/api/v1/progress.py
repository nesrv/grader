from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.progress import UserProgress
from app.schemas.progress import UserProgressCreate, UserProgressUpdate, UserProgressResponse, UserProgressList
from app.services.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=UserProgressResponse, status_code=status.HTTP_201_CREATED)
def create_progress(
    progress_create: UserProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создание записи о прогрессе пользователя"""
    # Проверяем, что пользователь создает запись для себя
    if progress_create.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя создавать записи прогресса для других пользователей"
        )
    
    # Проверяем, существует ли уже запись для этого урока
    existing_progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.lesson_id == progress_create.lesson_id
    ).first()
    
    if existing_progress:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Запись о прогрессе для этого урока уже существует"
        )
    
    # Создаем запись о прогрессе
    db_progress = UserProgress(**progress_create.dict())
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.get("/", response_model=UserProgressList)
def read_user_progress(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение списка прогресса текущего пользователя"""
    query = db.query(UserProgress).filter(UserProgress.user_id == current_user.id)
    total = query.count()
    progress = query.offset(skip).limit(limit).all()
    return {"progress": progress, "total": total}

@router.get("/{progress_id}", response_model=UserProgressResponse)
def read_progress(
    progress_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение записи о прогрессе по ID"""
    db_progress = db.query(UserProgress).filter(
        UserProgress.id == progress_id,
        UserProgress.user_id == current_user.id
    ).first()
    
    if not db_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прогрессе с ID {progress_id} не найдена"
        )
    
    return db_progress

@router.put("/{progress_id}", response_model=UserProgressResponse)
def update_progress(
    progress_id: int,
    progress_update: UserProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновление записи о прогрессе"""
    db_progress = db.query(UserProgress).filter(
        UserProgress.id == progress_id,
        UserProgress.user_id == current_user.id
    ).first()
    
    if not db_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись о прогрессе с ID {progress_id} не найдена"
        )
    
    # Обновляем поля
    update_data = progress_update.dict(exclude_unset=True)
    
    # Если урок завершен, устанавливаем дату завершения
    if "completed" in update_data and update_data["completed"] and not db_progress.completed:
        update_data["completed_at"] = datetime.utcnow()
    
    # Обновляем время последней попытки
    if "attempts" in update_data and update_data["attempts"] > db_progress.attempts:
        update_data["last_attempt_at"] = datetime.utcnow()
    
    # Обновляем поля
    for key, value in update_data.items():
        setattr(db_progress, key, value)
    
    # Если пользователь завершил урок, обновляем его XP
    if db_progress.completed and not db_progress.completed_at:
        # Получаем урок для определения награды XP
        lesson = db_progress.lesson
        current_user.xp_points += lesson.xp_reward
        db_progress.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_progress)
    return db_progress
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.education import Grade
from app.schemas import education as schemas
from app.deps.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.Grade])
def get_grades(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Получение списка всех грейдов"""
    grades = db.query(Grade).offset(skip).limit(limit).all()
    return grades

@router.get("/{grade_id}", response_model=schemas.Grade)
def get_grade(
    grade_id: int, 
    db: Session = Depends(get_db)
):
    """Получение информации о конкретном грейде по ID"""
    grade = db.query(Grade).filter(Grade.grade_id == grade_id).first()
    if grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    return grade

@router.post("/", response_model=schemas.Grade, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade: schemas.GradeCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Создание нового грейда"""
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.put("/{grade_id}", response_model=schemas.Grade)
def update_grade(
    grade_id: int, 
    grade_update: schemas.GradeUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Обновление информации о грейде"""
    db_grade = db.query(Grade).filter(Grade.grade_id == grade_id).first()
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    
    update_data = grade_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Удаление грейда"""
    db_grade = db.query(Grade).filter(Grade.grade_id == grade_id).first()
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    
    db.delete(db_grade)
    db.commit()
    return None
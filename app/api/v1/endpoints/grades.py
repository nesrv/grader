from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.education import Grade
from app.models.user import User
from app.schemas import education as schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Grade])
def get_grades(
    profession_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Получение списка грейдов, опционально по профессии"""
    query = db.query(Grade)
    if profession_id:
        query = query.filter(Grade.profession_id == profession_id)
    grades = query.all()
    return grades

@router.get("/{grade_id}", response_model=schemas.GradeDetail)
def get_grade(grade_id: int, db: Session = Depends(get_db)):
    """Получение детальной информации о грейде"""
    grade = db.query(Grade).filter(Grade.grade_id == grade_id).first()
    if grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    return grade

@router.post("/", response_model=schemas.Grade, status_code=status.HTTP_201_CREATED)
def create_grade(
    grade: schemas.GradeCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Создание нового грейда (только для администраторов)"""
    # Здесь должна быть проверка на права администратора
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.put("/{grade_id}", response_model=schemas.Grade)
def update_grade(
    grade_id: int,
    grade: schemas.GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновление грейда (только для администраторов)"""
    # Здесь должна быть проверка на права администратора
    db_grade = db.query(Grade).filter(Grade.grade_id == grade_id).first()
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    
    for key, value in grade.dict().items():
        setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.delete("/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удаление грейда (только для администраторов)"""
    # Здесь должна быть проверка на права администратора
    db_grade = db.query(Grade).filter(Grade.grade_id == grade_id).first()
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    
    db.delete(db_grade)
    db.commit()
    return None
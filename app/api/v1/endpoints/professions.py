from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.education import Profession
from app.models.user import User
from app.schemas import education as schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Profession])
def get_professions(db: Session = Depends(get_db)):
    """Получение списка всех профессий"""
    professions = db.query(Profession).all()
    return professions

@router.get("/{profession_id}", response_model=schemas.ProfessionDetail)
def get_profession(profession_id: int, db: Session = Depends(get_db)):
    """Получение детальной информации о профессии"""
    profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if profession is None:
        raise HTTPException(status_code=404, detail="Профессия не найдена")
    return profession

@router.post("/", response_model=schemas.Profession, status_code=status.HTTP_201_CREATED)
def create_profession(
    profession: schemas.ProfessionCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Создание новой профессии (только для администраторов)"""
    # Здесь должна быть проверка на права администратора
    db_profession = Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    db.refresh(db_profession)
    return db_profession

@router.put("/{profession_id}", response_model=schemas.Profession)
def update_profession(
    profession_id: int,
    profession: schemas.ProfessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновление профессии (только для администраторов)"""
    # Здесь должна быть проверка на права администратора
    db_profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Профессия не найдена")
    
    for key, value in profession.dict().items():
        setattr(db_profession, key, value)
    
    db.commit()
    db.refresh(db_profession)
    return db_profession

@router.delete("/{profession_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profession(
    profession_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удаление профессии (только для администраторов)"""
    # Здесь должна быть проверка на права администратора
    db_profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Профессия не найдена")
    
    db.delete(db_profession)
    db.commit()
    return None
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.education import Profession, Grade
from app.schemas.education import Profession as ProfessionSchema
from app.schemas.education import ProfessionCreate, ProfessionUpdate, ProfessionSimple
from app.schemas.education import Grade as GradeSchema
from app.schemas.education import GradeCreate, GradeUpdate
from app.deps.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProfessionSchema])
def get_professions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получение списка всех специальностей с их грейдами"""
    professions = db.query(Profession).offset(skip).limit(limit).all()
    return professions

@router.post("/", response_model=ProfessionSchema, status_code=status.HTTP_201_CREATED)
def create_profession(profession: ProfessionCreate, db: Session = Depends(get_db)):
    """Создание новой специальности"""
    db_profession = Profession(**profession.dict())
    db.add(db_profession)
    db.commit()
    db.refresh(db_profession)
    return db_profession

@router.get("/{profession_id}", response_model=ProfessionSchema)
def get_profession(profession_id: int, db: Session = Depends(get_db)):
    """Получение информации о конкретной специальности по ID"""
    profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if profession is None:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    return profession

@router.put("/{profession_id}", response_model=ProfessionSchema)
def update_profession(profession_id: int, profession_update: ProfessionUpdate, db: Session = Depends(get_db)):
    """Обновление информации о специальности"""
    db_profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    
    update_data = profession_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profession, key, value)
    
    db.commit()
    db.refresh(db_profession)
    return db_profession

@router.delete("/{profession_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profession(profession_id: int, db: Session = Depends(get_db)):
    """Удаление специальности"""
    db_profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if db_profession is None:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    
    db.delete(db_profession)
    db.commit()
    return None

# Эндпоинты для работы с грейдами

@router.get("/{profession_id}/grades", response_model=List[GradeSchema])
def get_profession_grades(profession_id: int, db: Session = Depends(get_db)):
    """Получение всех грейдов для конкретной специальности"""
    profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if profession is None:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    
    return profession.grades

@router.post("/{profession_id}/grades", response_model=GradeSchema, status_code=status.HTTP_201_CREATED)
def create_profession_grade(profession_id: int, grade: GradeCreate, db: Session = Depends(get_db)):
    """Создание нового грейда для специальности"""
    profession = db.query(Profession).filter(Profession.profession_id == profession_id).first()
    if profession is None:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/{profession_id}/grades/{grade_id}", response_model=GradeSchema)
def get_profession_grade(profession_id: int, grade_id: int, db: Session = Depends(get_db)):
    """Получение информации о конкретном грейде специальности"""
    grade = db.query(Grade).filter(
        Grade.profession_id == profession_id,
        Grade.grade_id == grade_id
    ).first()
    
    if grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    
    return grade

@router.put("/{profession_id}/grades/{grade_id}", response_model=GradeSchema)
def update_profession_grade(profession_id: int, grade_id: int, grade_update: GradeUpdate, db: Session = Depends(get_db)):
    """Обновление информации о грейде"""
    db_grade = db.query(Grade).filter(
        Grade.profession_id == profession_id,
        Grade.grade_id == grade_id
    ).first()
    
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    
    update_data = grade_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_grade, key, value)
    
    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.delete("/{profession_id}/grades/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profession_grade(profession_id: int, grade_id: int, db: Session = Depends(get_db)):
    """Удаление грейда"""
    db_grade = db.query(Grade).filter(
        Grade.profession_id == profession_id,
        Grade.grade_id == grade_id
    ).first()
    
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Грейд не найден")
    
    db.delete(db_grade)
    db.commit()
    return None
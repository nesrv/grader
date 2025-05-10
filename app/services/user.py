from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth import get_password_hash

def get_user(db: Session, user_id: int):
    """Получение пользователя по ID"""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение списка пользователей"""
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """Создание нового пользователя"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name if hasattr(user, 'first_name') else None,
        last_name=user.last_name if hasattr(user, 'last_name') else None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """Обновление данных пользователя"""
    db_user = get_user(db, user_id)
    
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Удаление пользователя"""
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return {"message": "Пользователь успешно удален"}
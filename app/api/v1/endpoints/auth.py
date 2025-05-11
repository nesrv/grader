from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.user import User
from app.schemas import user as schemas
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрация нового пользователя"""
    try:
        # Проверяем, существует ли пользователь с таким email или username
        db_user = db.query(User).filter(
            or_(User.email == user_data.email, User.username == user_data.username)
        ).first()
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким email или именем пользователя уже существует"
            )
        
        # Создаем нового пользователя
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    except HTTPException:
        # Пробрасываем HTTPException дальше
        raise
    except Exception as e:
        # Логируем ошибку и возвращаем более информативное сообщение
        print(f"Error during registration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при регистрации: {str(e)}"
        )

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Аутентификация пользователя и получение токена"""
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверное имя пользователя или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": str(user.user_id)})
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Пробрасываем HTTPException дальше
        raise
    except Exception as e:
        # Логируем ошибку и возвращаем более информативное сообщение
        print(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при входе: {str(e)}"
        )
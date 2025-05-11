from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.models.education import Profession, Grade
from app.models.user import User
from app.core.security import get_password_hash

def init_db():
    """Инициализация базы данных начальными данными"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Проверяем, есть ли уже данные в базе
    if db.query(User).filter(User.username == "superadmin").first() is None:
        # Создаем администратора
        admin_user = User(
            username="superadmin",
            email="admin@itgrader.ru",
            password_hash=get_password_hash("superadmin"),
            first_name="Admin",
            last_name="User",
            is_active=True
            # Убираем поле is_admin, так как его нет в базе данных
        )
        db.add(admin_user)
        db.commit()
        print("Создан администратор: superadmin")
    
    # Создаем специальности, если их нет
    professions_data = [
        {"name": "Python-бэкендер", "description": "Разработка серверной части веб-приложений на Python"},
        {"name": "Python-аналитик", "description": "Анализ данных с использованием Python"},
        {"name": "Базы данных для бэкендеров", "description": "Работа с базами данных в контексте бэкенд-разработки"}
    ]
    
    # Список грейдов для каждой специальности
    grades_data = [
        {"name": "Стажер", "level": 1, "description": "Начальный уровень, основы языка и технологий"},
        {"name": "Джун", "level": 2, "description": "Базовые навыки, простые задачи под руководством"},
        {"name": "Джун+", "level": 3, "description": "Уверенное владение базовыми технологиями, самостоятельные задачи"},
        {"name": "Мидл", "level": 4, "description": "Опытный разработчик, сложные задачи, архитектурные решения"},
        {"name": "Синьор", "level": 5, "description": "Эксперт, лидерство, стратегические решения"}
    ]
    
    # Добавляем специальности и грейды
    for prof_data in professions_data:
        # Проверяем, существует ли уже такая специальность
        existing_profession = db.query(Profession).filter(Profession.name == prof_data["name"]).first()
        
        if existing_profession is None:
            # Создаем новую специальность
            profession = Profession(**prof_data)
            db.add(profession)
            db.commit()
            db.refresh(profession)
            print(f"Создана специальность: {profession.name}")
            
            # Добавляем грейды для этой специальности
            for grade_data in grades_data:
                grade = Grade(
                    **grade_data,
                    profession_id=profession.profession_id
                )
                db.add(grade)
            
            db.commit()
            print(f"Добавлены грейды для специальности: {profession.name}")
        else:
            # Проверяем, есть ли уже грейды для этой специальности
            existing_grades = db.query(Grade).filter(Grade.profession_id == existing_profession.profession_id).all()
            
            if not existing_grades:
                # Добавляем грейды для существующей специальности
                for grade_data in grades_data:
                    grade = Grade(
                        **grade_data,
                        profession_id=existing_profession.profession_id
                    )
                    db.add(grade)
                
                db.commit()
                print(f"Добавлены грейды для существующей специальности: {existing_profession.name}")
    
    db.close()
    print("Инициализация базы данных завершена")

if __name__ == "__main__":
    init_db()
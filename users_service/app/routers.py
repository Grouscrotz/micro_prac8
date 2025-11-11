from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import UserRegister, UserLogin
from .schemas import DBUser

router = APIRouter(prefix="/api/users", tags=["Users"])

# ЗАГЛУШКА — по методичке: полная изоляция от других сервисов
USERS_MEDICINES_URL = "http://medicines_service:8000/api/medicines"


@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = DBUser(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    return {"message": "Зарегистрирован"}


@router.post("/login")
def login(login: UserLogin, db: Session = Depends(get_db)):  # УБРАЛИ async
    user = db.query(DBUser).filter(DBUser.email == login.email).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")
    
    # ЗАГЛУШКА: вместо вызова medicines_service
    medicines = []  # Пустой список — как в методичке
    has_medicines = len(medicines) > 0
    return {
        "user_id": str(user.user_id),
        "name": user.name,
        "has_medicines": has_medicines,
        "medicines_count": len(medicines)
    }


@router.get("/profile/{user_id}")
def profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if not user:
        raise HTTPException(404)
    return {"name": user.name, "email": user.email}
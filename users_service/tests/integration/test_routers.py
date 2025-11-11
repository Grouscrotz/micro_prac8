import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.routers import register, login, profile
from app.models import UserRegister, UserLogin
from app.schemas import DBUser
from app.database import Base

# === ТВОЯ ТЕСТОВАЯ БД ===
TEST_DB_URL = "postgresql://testuser:testpass@localhost:5433/test_pharmacy_db"
engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаём таблицы
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db():
    session = TestingSessionLocal()
    # ОЧИЩАЕМ БД ПЕРЕД ТЕСТАМИ — как в методичке (чистое состояние)
    session.query(DBUser).delete()
    session.commit()
    yield session
    session.close()


@pytest.fixture(scope="session")
def user1():
    return UserRegister(email="user1@example.com", name="User One")


@pytest.fixture(scope="session")
def user2():
    return UserRegister(email="user2@example.com", name="User Two")


@pytest.fixture(scope="session")
def login_user1():
    return UserLogin(email="user1@example.com")


@pytest.fixture(scope="session")
def login_unknown():
    return UserLogin(email="unknown@example.com")


# === ТЕСТЫ — ПО МЕТОДИЧКЕ ===

def test_register_first_user(user1, db):
    response = register(user=user1, db=db)
    assert response == {"message": "Зарегистрирован"}
    u = db.query(DBUser).filter(DBUser.email == "user1@example.com").first()
    assert u.name == "User One"


def test_register_first_user_repeat(user1, db):
    try:
        register(user=user1, db=db)
    except Exception:
        db.rollback()  # Очищаем состояние
    else:
        assert False, "Должна быть ошибка уникальности"


def test_login_success(login_user1, db):
    response = login(login=login_user1, db=db)
    assert response["name"] == "User One"
    assert response["has_medicines"] is False
    assert response["medicines_count"] == 0
    assert "user_id" in response


def test_profile_success(db):
    user = db.query(DBUser).filter(DBUser.email == "user1@example.com").first()
    response = profile(user_id=str(user.user_id), db=db)
    assert response["name"] == "User One"
    assert response["email"] == "user1@example.com"



def test_register_second_user(user2, db):
    response = register(user=user2, db=db)
    assert response == {"message": "Зарегистрирован"}
    users = db.query(DBUser).all()
    assert len(users) == 2
    assert any(u.email == "user2@example.com" for u in users)
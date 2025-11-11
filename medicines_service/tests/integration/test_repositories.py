import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from app.models import Medicine
from app.schemas import DBMedicine, Base
from app.repositories import MedicineRepo
from app.settings import settings  # Но используем тестовый URL

# Тестовый engine (замените на тестовую БД)
TEST_DB_URL = "postgresql://testuser:testpass@localhost:5433/test_pharmacy_db"
engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)  # Создаём таблицы
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)  # Чистим после

def test_create_and_get_medicine(test_db):
    repo = MedicineRepo(test_db)
    med_data = Medicine(name="Integration Test Med", description="Desc", price=15.0)
    created_med = repo.create(med_data)
    assert created_med.medicine_id is not None

    fetched_med = repo.get_by_id(str(created_med.medicine_id))
    assert fetched_med.name == "Integration Test Med"
import pytest
from datetime import datetime
from app.models import Medicine  # Предполагаемый путь
from pydantic_core import ValidationError  # ← правильный импорт!

def test_medicine_creation():
    med = Medicine(
        name="Aspirin",
        description="Pain relief",
        price=10.5,
        in_stock=True,
        updated_at=datetime.utcnow()
    )
    assert med.name == "Aspirin"
    assert med.price == 10.5
    assert med.in_stock is True

def test_medicine_missing_required():
    with pytest.raises(ValidationError):
        Medicine(description="No name", price=0)  # Нет name

def test_medicine_invalid_price():
    with pytest.raises(ValidationError):
        Medicine(name="Invalid", description="", price=-5)  # Отрицательная цена
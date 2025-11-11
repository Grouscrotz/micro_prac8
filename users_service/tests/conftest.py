# users_service/tests/conftest.py
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Мокаем create_all ДО импорта
with patch("app.database.Base.metadata.create_all"):
    from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
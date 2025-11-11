import pytest
from pydantic import ValidationError

from app.models import UserRegister, UserLogin


def test_user_register_valid():
    user = UserRegister(email="test@example.com", name="Test User")
    assert user.email == "test@example.com"
    assert user.name == "Test User"


def test_user_register_missing_email():
    with pytest.raises(ValidationError):
        UserRegister(name="Test User")


def test_user_register_missing_name():
    with pytest.raises(ValidationError):
        UserRegister(email="test@example.com")


def test_user_login_valid():
    login = UserLogin(email="test@example.com")
    assert login.email == "test@example.com"


def test_user_login_missing_email():
    with pytest.raises(ValidationError):
        UserLogin()
import pytest
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister, UserLogin
from app.models.user import RoleEnum

def test_register_new_user_success(db_session):
    service = AuthService(db_session)
    user_data = UserRegister(
        name="John Doe",
        email="john@example.com",
        password="Password123!",
        role=RoleEnum.USER
    )
    result = service.register(user_data)
    assert result.user.email == "john@example.com"
    assert result.user.name == "John Doe"
    assert result.user.role == RoleEnum.USER
    assert result.access_token is not None

def test_register_duplicate_email_raises_value_error(db_session):
    service = AuthService(db_session)
    user_data = UserRegister(
        name="John Doe",
        email="john@example.com",
        password="Password123!"
    )
    service.register(user_data)
    
    with pytest.raises(ValueError, match="User with this email already exists"):
        service.register(user_data)

def test_login_valid_credentials_success(db_session):
    service = AuthService(db_session)
    user_data = UserRegister(
        name="Jane Doe",
        email="jane@example.com",
        password="Password123!"
    )
    service.register(user_data)
    
    login_data = UserLogin(email="jane@example.com", password="Password123!")
    result = service.login(login_data)
    assert result.user.email == "jane@example.com"
    assert result.access_token is not None

def test_login_wrong_password_raises_value_error(db_session):
    service = AuthService(db_session)
    user_data = UserRegister(
        name="Jane Doe",
        email="jane@example.com",
        password="Password123!"
    )
    service.register(user_data)
    
    login_data = UserLogin(email="jane@example.com", password="WrongPassword!")
    with pytest.raises(ValueError, match="Invalid email or password"):
        service.login(login_data)

def test_login_unregistered_email_raises_value_error(db_session):
    service = AuthService(db_session)
    login_data = UserLogin(email="nobody@example.com", password="Password123!")
    with pytest.raises(ValueError, match="Invalid email or password"):
        service.login(login_data)

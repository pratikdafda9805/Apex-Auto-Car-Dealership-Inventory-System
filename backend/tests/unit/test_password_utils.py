import pytest
from app.utils.password_utils import hash_password, verify_password

def test_hash_password_returns_hashed_string():
    password = "SecretPassword123!"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

def test_verify_correct_password_returns_true():
    password = "SecretPassword123!"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True

def test_verify_wrong_password_returns_false():
    password = "SecretPassword123!"
    hashed = hash_password(password)
    assert verify_password("WrongPassword!", hashed) is False

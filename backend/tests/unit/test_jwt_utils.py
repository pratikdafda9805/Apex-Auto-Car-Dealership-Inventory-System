import pytest
import time
from app.utils.jwt_utils import create_access_token, decode_access_token

def test_create_access_token_returns_jwt_string():
    data = {"sub": "user-123", "role": "user"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token.split(".")) == 3  # Valid JWT format: header.payload.signature

def test_decode_valid_access_token_returns_payload():
    data = {"sub": "user-456", "role": "admin"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "user-456"
    assert payload.get("role") == "admin"
    assert "exp" in payload

def test_decode_invalid_token_returns_none():
    invalid_token = "invalid.token.string"
    payload = decode_access_token(invalid_token)
    assert payload is None

def test_decode_expired_token_returns_none():
    data = {"sub": "user-789", "role": "user"}
    # Pass 1-second expiration and wait 2 seconds
    token = create_access_token(data, expires_delta_seconds=-10)
    payload = decode_access_token(token)
    assert payload is None

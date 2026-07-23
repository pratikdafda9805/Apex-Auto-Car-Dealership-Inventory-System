import pytest

def test_register_user_success(client):
    payload = {
        "name": "Alice Smith",
        "email": "alice@test.com",
        "password": "Password123!"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "alice@test.com"
    assert data["user"]["role"] == "user"

def test_register_duplicate_email_returns_400(client):
    payload = {
        "name": "Alice Smith",
        "email": "alice@test.com",
        "password": "Password123!"
    }
    client.post("/api/auth/register", json=payload)
    
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_user_success(client):
    reg_payload = {
        "name": "Bob Builder",
        "email": "bob@test.com",
        "password": "Password123!"
    }
    client.post("/api/auth/register", json=reg_payload)

    login_payload = {
        "email": "bob@test.com",
        "password": "Password123!"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "bob@test.com"

def test_login_wrong_password_returns_401(client):
    reg_payload = {
        "name": "Bob Builder",
        "email": "bob@test.com",
        "password": "Password123!"
    }
    client.post("/api/auth/register", json=reg_payload)

    login_payload = {
        "email": "bob@test.com",
        "password": "WrongPassword!"
    }
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

import pytest

def test_get_vehicles_unauthenticated_returns_403(client):
    response = client.get("/api/vehicles")
    assert response.status_code in (401, 403)

def test_create_vehicle_as_admin_success(client, auth_headers_admin):
    headers, _ = auth_headers_admin
    payload = {
        "make": "Tesla",
        "model": "Model 3",
        "year": 2024,
        "category": "EV",
        "price": 38990.0,
        "quantity": 10,
        "color": "White"
    }
    response = client.post("/api/vehicles", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["make"] == "Tesla"
    assert data["quantity"] == 10

def test_create_vehicle_as_user_forbidden(client, auth_headers_user):
    headers, _ = auth_headers_user
    payload = {
        "make": "Tesla",
        "model": "Model 3",
        "year": 2024,
        "category": "EV",
        "price": 38990.0,
        "quantity": 10
    }
    response = client.post("/api/vehicles", json=payload, headers=headers)
    assert response.status_code == 403

def test_get_all_vehicles_authenticated(client, auth_headers_user, auth_headers_admin):
    admin_headers, _ = auth_headers_admin
    client.post("/api/vehicles", json={"make": "Toyota", "model": "Camry", "year": 2024, "category": "Sedan", "price": 28000, "quantity": 5}, headers=admin_headers)

    user_headers, _ = auth_headers_user
    response = client.get("/api/vehicles", headers=user_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_search_vehicles_authenticated(client, auth_headers_user, auth_headers_admin):
    admin_headers, _ = auth_headers_admin
    client.post("/api/vehicles", json={"make": "Honda", "model": "Civic", "year": 2023, "category": "Sedan", "price": 24000, "quantity": 4}, headers=admin_headers)
    client.post("/api/vehicles", json={"make": "BMW", "model": "X5", "year": 2024, "category": "SUV", "price": 65000, "quantity": 2}, headers=admin_headers)

    user_headers, _ = auth_headers_user
    res = client.get("/api/vehicles/search?category=SUV", headers=user_headers)
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["make"] == "BMW"

def test_update_vehicle_as_admin(client, auth_headers_admin):
    admin_headers, _ = auth_headers_admin
    created = client.post("/api/vehicles", json={"make": "Mazda", "model": "CX-5", "year": 2023, "category": "SUV", "price": 30000, "quantity": 3}, headers=admin_headers).json()

    res = client.put(f"/api/vehicles/{created['id']}", json={"price": 28500}, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["price"] == 28500

def test_delete_vehicle_as_admin(client, auth_headers_admin):
    admin_headers, _ = auth_headers_admin
    created = client.post("/api/vehicles", json={"make": "Nissan", "model": "Altima", "year": 2022, "category": "Sedan", "price": 22000, "quantity": 1}, headers=admin_headers).json()

    res = client.delete(f"/api/vehicles/{created['id']}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["message"] == "Vehicle deleted successfully"

def test_purchase_vehicle_as_user(client, auth_headers_admin, auth_headers_user):
    admin_headers, _ = auth_headers_admin
    user_headers, _ = auth_headers_user
    created = client.post("/api/vehicles", json={"make": "Chevy", "model": "Malibu", "year": 2023, "category": "Sedan", "price": 25000, "quantity": 4}, headers=admin_headers).json()

    res = client.post(f"/api/vehicles/{created['id']}/purchase", json={"quantity": 1}, headers=user_headers)
    assert res.status_code == 200
    assert res.json()["vehicle"]["quantity"] == 3

def test_purchase_out_of_stock_returns_400(client, auth_headers_admin, auth_headers_user):
    admin_headers, _ = auth_headers_admin
    user_headers, _ = auth_headers_user
    created = client.post("/api/vehicles", json={"make": "Ford", "model": "Focus", "year": 2020, "category": "Compact", "price": 15000, "quantity": 0}, headers=admin_headers).json()

    res = client.post(f"/api/vehicles/{created['id']}/purchase", json={"quantity": 1}, headers=user_headers)
    assert res.status_code == 400
    assert "Insufficient stock" in res.json()["detail"]

def test_restock_vehicle_as_admin(client, auth_headers_admin):
    admin_headers, _ = auth_headers_admin
    created = client.post("/api/vehicles", json={"make": "Ford", "model": "Focus", "year": 2020, "category": "Compact", "price": 15000, "quantity": 0}, headers=admin_headers).json()

    res = client.post(f"/api/vehicles/{created['id']}/restock", json={"quantity": 5}, headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["vehicle"]["quantity"] == 5

def test_restock_as_regular_user_forbidden(client, auth_headers_admin, auth_headers_user):
    admin_headers, _ = auth_headers_admin
    user_headers, _ = auth_headers_user
    created = client.post("/api/vehicles", json={"make": "Ford", "model": "Focus", "year": 2020, "category": "Compact", "price": 15000, "quantity": 0}, headers=admin_headers).json()

    res = client.post(f"/api/vehicles/{created['id']}/restock", json={"quantity": 5}, headers=user_headers)
    assert res.status_code == 403

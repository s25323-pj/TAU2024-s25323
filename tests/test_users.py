from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_user_valid():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Jan Kowalski"

def test_get_user_invalid():
    response = client.get("/users/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user():
    new_user = {"name": "Piotr Nowak", "email": "piotr@nowak.pl"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    assert response.json()["name"] == new_user["name"]

def test_create_user_invalid():
    incomplete_user = {"name": "Invalid User"}
    response = client.post("/users", json=incomplete_user)
    assert response.status_code == 422

def test_update_user():
    updated_user = {"name": "Updated Name", "email": "updated@email.com"}
    response = client.put("/users/1", json=updated_user)
    assert response.status_code == 200
    assert response.json()["name"] == updated_user["name"]

def test_update_user_invalid():
    updated_user = {"name": "Invalid User", "email": "invalid@email.com"}
    response = client.put("/users/99", json=updated_user)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 204
    response = client.get("/users/1")
    assert response.status_code == 404

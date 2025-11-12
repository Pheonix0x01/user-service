from fastapi.testclient import TestClient

def test_create_user(client):
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "securepassword",
        "preferences": {
            "email": True,
            "push": False
        }
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    
    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["email"] == "john@example.com"
    assert response.json()["data"]["name"] == "John Doe"
    assert "id" in response.json()["data"]

def test_create_duplicate_user(client):
    user_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "password123",
        "preferences": {"email": True, "push": True}
    }
    
    client.post("/api/v1/users/", json=user_data)
    
    response = client.post("/api/v1/users/", json=user_data)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_update_push_token(client):
    user_data = {
        "name": "Push User",
        "email": "pushuser@example.com",
        "password": "password123",
        "preferences": {"email": True, "push": True}
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["data"]["id"]
    
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "pushuser@example.com", "password": "password123"}
    )
    token = login_response.json()["data"]["access_token"]
    
    response = client.put(
        f"/api/v1/users/{user_id}/push-token",
        json={"push_token": "new_push_token_123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["data"]["push_token"] == "new_push_token_123"

def test_update_preferences(client):
    user_data = {
        "name": "Pref User",
        "email": "prefuser@example.com",
        "password": "password123",
        "preferences": {"email": True, "push": True}
    }
    
    create_response = client.post("/api/v1/users/", json=user_data)
    user_id = create_response.json()["data"]["id"]
    
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "prefuser@example.com", "password": "password123"}
    )
    token = login_response.json()["data"]["access_token"]
    
    response = client.put(
        f"/api/v1/users/{user_id}/preferences",
        json={"preferences": {"email": False, "push": False}},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["data"]["preferences"]["email"] is False
    assert response.json()["data"]["preferences"]["push"] is False
from fastapi.testclient import TestClient
from typing import Tuple
from models import User

def test_login(client: TestClient, user_credentials: Tuple[str, str]):
    """Test the login endpoint."""
    username, password = user_credentials
    response = client.post("/api/login", data={"username": username, "password": password})
    assert response.status_code == 200, "Should return 200 for valid credentials"
    token = response.json().get("access_token")
    assert token is not None, "Token should be returned for valid credentials"


def test_login_invalid_credentials(client: TestClient):
    """Test the login endpoint with invalid credentials."""
    response = client.post("/api/login", data={"username": "admin", "password": "wrongpassword"})
    assert response.status_code == 401, "Should return 401 for invalid credentials"


def test_login_nonexistent_user(client: TestClient):
    """Test the login endpoint with a nonexistent user."""
    response = client.post("/api/login", data={"username": "nonexistent", "password": "password"})
    assert response.status_code == 401, "Should return 401 for nonexistent user"
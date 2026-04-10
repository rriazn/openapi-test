from fastapi.testclient import TestClient
from models import Exercise

def test_list_exercises(client: TestClient, token: str, exercise: Exercise):
    response = client.get("/api/exercises", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert any(e["id"] == exercise.id for e in response.json()["exercises"]), "Created exercise should be in the list"

from fastapi.testclient import TestClient
from typing import Tuple

from models import Exercise, Routine, User

def test_list_routines(client: TestClient, token: str, routine: Routine):
    response = client.get("/api/routines", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert any(w["id"] == routine.id for w in response.json()["routines"]), "Created routine should be in the list"


def test_list_routine_not_owned(client: TestClient, token: str, routine_other_user: Routine):
    response = client.get("/api/routines", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert all(w["id"] != routine_other_user.id for w in response.json()["routines"]), "Routine owned by another user should not be in the list"


def test_get_routine_details(client: TestClient, token: str, routine: Routine, exercise: Exercise):
    response = client.get(f"/api/routines/{routine.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert any(e == exercise.name for e in response.json()["exercises"]), "Exercise in routine should be listed in routine details"
    assert response.json()["owner"] == routine.user_name, "Routine owner should match"
    assert response.json()["name"] == routine.name, "Routine name should match"


def test_get_routine_details_not_owned(client: TestClient, token: str, routine_other_user: Routine):
    response = client.get(f"/api/routines/{routine_other_user.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, "Should return 403 for routine not owned by user"


def test_get_routine_details_does_not_exist(client: TestClient, token: str):
    response = client.get(f"/api/routines/999999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Should return 404 for routine that does not exist"


def test_create_routine(client: TestClient, user_instance: Tuple[User, str], exercise: Exercise):
    response = client.post("/api/routines", json={
        "routine_name": "test routine",
        "exercise_ids": [exercise.id]
    }, headers={"Authorization": f"Bearer {user_instance[1]}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test routine", "Routine name should match"
    assert data["owner"] == user_instance[0].username, "Routine owner should match"
    assert any(e == exercise.name for e in data["exercises"]), "Created exercise should be in the routine details"


def test_create_empty_routine(client: TestClient, user_instance: Tuple[User, str]):
    response = client.post("/api/routines", json={
        "routine_name": "empty routine",
        "exercise_ids": []
    }, headers={"Authorization": f"Bearer {user_instance[1]}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "empty routine", "Routine name should match"
    assert data["owner"] == user_instance[0].username, "Routine owner should match"
    assert len(data["exercises"]) == 0, "Routine should have no exercises"


def test_create_routine_exercise_does_not_exist(client: TestClient, token: str):
    response = client.post("/api/routines", json={
        "routine_name": "test routine",
        "exercise_ids": [999999]
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Should return 404 when trying to create routine with non-existent exercise"


def test_delete_routine(client: TestClient, token: str, routine: Routine):
    response = client.delete(f"/api/routines/{routine.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, "Should return 200 for successful deletion"
    assert response.json()["message"] == "Routine deleted successfully", "Response message should indicate successful deletion"

    # Verify routine is actually deleted
    response = client.get(f"/api/routines/{routine.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Deleted routine should not be found"


def test_delete_routine_not_owned(client: TestClient, token: str, routine_other_user: Routine):
    response = client.delete(f"/api/routines/{routine_other_user.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, "Should return 403 when trying to delete routine not owned by user"


def test_delete_routine_does_not_exist(client: TestClient, token: str):
    response = client.delete(f"/api/routines/999999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Should return 404 when trying to delete routine that does not exist"
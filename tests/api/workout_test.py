from fastapi.testclient import TestClient
from typing import Tuple

from models import Exercise, Workout, User

def test_list_workouts(client: TestClient, token: str, workout: Workout):
    response = client.get("/api/workouts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert any(w["id"] == workout.id for w in response.json()["workouts"]), "Created workout should be in the list"


def test_list_workout_not_owned(client: TestClient, token: str, workout_other_user: Workout):
    response = client.get("/api/workouts", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert all(w["id"] != workout_other_user.id for w in response.json()["workouts"]), "Workout owned by another user should not be in the list"


def test_get_workout_details(client: TestClient, token: str, workout: Workout, exercise: Exercise):
    response = client.get(f"/api/workouts/{workout.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert any(e == exercise.name for e in response.json()["exercises"]), "Exercise in workout should be listed in workout details"
    assert response.json()["owner"] == workout.user_name, "Workout owner should match"
    assert response.json()["name"] == workout.name, "Workout name should match"


def test_get_workout_details_not_owned(client: TestClient, token: str, workout_other_user: Workout):
    response = client.get(f"/api/workouts/{workout_other_user.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, "Should return 403 for workout not owned by user"


def test_get_workout_details_does_not_exist(client: TestClient, token: str):
    response = client.get(f"/api/workouts/999999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Should return 404 for workout that does not exist"


def test_create_workout(client: TestClient, user_instance: Tuple[User, str], exercise: Exercise):
    response = client.post("/api/workouts", json={
        "workout_name": "test workout",
        "exercise_ids": [exercise.id]
    }, headers={"Authorization": f"Bearer {user_instance[1]}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test workout", "Workout name should match"
    assert data["owner"] == user_instance[0].username, "Workout owner should match"
    assert any(e == exercise.name for e in data["exercises"]), "Created exercise should be in the workout details"


def test_create_empty_workout(client: TestClient, user_instance: Tuple[User, str]):
    response = client.post("/api/workouts", json={
        "workout_name": "empty workout",
        "exercise_ids": []
    }, headers={"Authorization": f"Bearer {user_instance[1]}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "empty workout", "Workout name should match"
    assert data["owner"] == user_instance[0].username, "Workout owner should match"
    assert len(data["exercises"]) == 0, "Workout should have no exercises"


def test_create_workout_exercise_does_not_exist(client: TestClient, token: str):
    response = client.post("/api/workouts", json={
        "workout_name": "test workout",
        "exercise_ids": [999999]
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Should return 404 when trying to create workout with non-existent exercise"


def test_delete_workout(client: TestClient, token: str, workout: Workout):
    response = client.delete(f"/api/workouts/{workout.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, "Should return 200 for successful deletion"
    assert response.json()["message"] == "Workout deleted successfully", "Response message should indicate successful deletion"

    # Verify workout is actually deleted
    response = client.get(f"/api/workouts/{workout.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Deleted workout should not be found"


def test_delete_workout_not_owned(client: TestClient, token: str, workout_other_user: Workout):
    response = client.delete(f"/api/workouts/{workout_other_user.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403, "Should return 403 when trying to delete workout not owned by user"


def test_delete_workout_does_not_exist(client: TestClient, token: str):
    response = client.delete(f"/api/workouts/999999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404, "Should return 404 when trying to delete workout that does not exist"
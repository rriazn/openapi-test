from tests.integration.common import make_request
from .common import wait_for_api, authenticate_user, api_url
import json


def test_create_delete_workout():
    wait_for_api()

    # Authenticate user
    token = authenticate_user()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create workout
    response = make_request(f"{api_url()}/workouts", method="POST", headers={**headers, "Content-Type": "application/json"}, data=json.dumps({
        "workout_name": "workout to delete",
        "exercise_ids": []
    }))
    assert response["status"] == 200, "Should return 200 for workout creation"
    data = response["json"]()
    workout_id = data["id"]
    
    # Verify workout was created
    response = make_request(f"{api_url()}/workouts/{workout_id}", headers=headers)
    assert response["status"] == 200
    assert response["json"]()["name"] == "workout to delete", "Workout name should match"
    
    # Delete workout
    response = make_request(f"{api_url()}/workouts/{workout_id}", method="DELETE", headers=headers)
    assert response["status"] == 200
    assert response["json"]()["message"] == "Workout deleted successfully", "Delete message should match"
    
    # Verify workout was deleted
    response = make_request(f"{api_url()}/workouts/{workout_id}", headers=headers)
    assert response["status"] == 404, "Should return 404 for deleted workout"
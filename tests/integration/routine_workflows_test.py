from tests.integration.common import make_request
from .common import wait_for_api, authenticate_user, api_url
import json


def cleanup_test_environment(token: str, created_routines: list):
    """Cleanup any test data created during integration tests."""
    headers = {"Authorization": f"Bearer {token}"}
    for routine_id in created_routines:
        response = make_request(f"{api_url()}/routines/{routine_id}", method="DELETE", headers=headers)
        if response["status"] != 200:
            print(f"Failed to delete routine with ID {routine_id}: {response['content']}")


def test_create_delete_routine():
    wait_for_api()

    # Authenticate user
    token = authenticate_user()
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Create routine
        response = make_request(f"{api_url()}/routines", method="POST", headers={**headers, "Content-Type": "application/json"}, data=json.dumps({
            "routine_name": "routine to delete",
            "exercise_ids": []
        }))
        assert response["status"] == 200, "Should return 200 for routine creation"
        data = response["json"]()
        routine_id = data["id"]
        
        # Verify routine was created
        response = make_request(f"{api_url()}/routines/{routine_id}", headers=headers)
        assert response["status"] == 200
        assert response["json"]()["name"] == "routine to delete", "Routine name should match"
        
        # Delete routine
        response = make_request(f"{api_url()}/routines/{routine_id}", method="DELETE", headers=headers)
        assert response["status"] == 200
        assert response["json"]()["message"] == "Routine deleted successfully", "Delete message should match"
        
        # Verify routine was deleted
        response = make_request(f"{api_url()}/routines/{routine_id}", headers=headers)
        assert response["status"] == 404, "Should return 404 for deleted routine"
    except Exception as e:
        # Cleanup any created routines in case of test failure
        cleanup_test_environment(token, [routine_id])
        raise e


def test_create_edit_routine():
    wait_for_api()

    # Authenticate user
    token = authenticate_user()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        # Request existing exercises
        response = make_request(f"{api_url()}/exercises", headers=headers)
        assert response["status"] == 200
        exercises = response["json"]()["exercises"]

        # Create routine
        response = make_request(f"{api_url()}/routines", method="POST", headers={**headers, "Content-Type": "application/json"}, data=json.dumps({
            "routine_name": "routine to edit",
            "exercise_ids": [exercises[0]["id"]]
        }))
        assert response["status"] == 200, "Should return 200 for routine creation"
        data = response["json"]()
        routine_id = data["id"]
        assert any(e == exercises[0]["name"] for e in data["exercises"]), "Created exercise should be in the routine details"

        # Edit routine
        response = make_request(f"{api_url()}/routines/{routine_id}", method="PUT", headers={**headers, "Content-Type": "application/json"}, data=json.dumps({
            "routine_name": "edited routine",
            "exercise_add": [exercises[1]["id"]],
            "exercise_remove": [exercises[0]["id"]]
        }))
        assert response["status"] == 200, "Should return 200 for routine edit"
        data = response["json"]()
        assert data["name"] == "edited routine", "Routine name should be updated"
        assert any(e == exercises[1]["name"] for e in data["exercises"]), "Added exercise should be in the routine details"
        assert not any(e == exercises[0]["name"] for e in data["exercises"]), "Removed exercise should not be in the routine details"

        # Verify routine details after edit
        response = make_request(f"{api_url()}/routines/{routine_id}", headers=headers)
        assert response["status"] == 200
        data = response["json"]()
        assert data["name"] == "edited routine", "Routine name should match after edit"
        assert any(e == exercises[1]["name"] for e in data["exercises"]), "Added exercise should be in the routine details after edit"
        assert not any(e == exercises[0]["name"] for e in data["exercises"]), "Removed exercise should not be in the routine details after edit"
    finally:
        # Cleanup created routine
        cleanup_test_environment(token, [routine_id])
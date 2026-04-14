from tests.integration.common import make_request
from .common import wait_for_api, authenticate_user, api_url
import json


def test_create_delete_routine():
    wait_for_api()

    # Authenticate user
    token = authenticate_user()
    headers = {"Authorization": f"Bearer {token}"}
    
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
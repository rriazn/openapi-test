"""Test Authentication and Authorization."""

import pytest
from .common import api_url, make_request, wait_for_api

pytestmark = pytest.mark.integration

def test_authentication_success():
    """Test that authentication works correctly."""
    wait_for_api()

    # Test login with correct credentials
    response = make_request(f"{api_url()}/login", method="POST", data={"username": "admin", "password": "password"})
    assert response["status"] == 200, "Should return 200 for valid credentials"

    token = response["json"]().get("access_token")
    assert token is not None, "Token should be returned for valid credentials"

    # Verify that protected endpoint is accessible with valid token
    protected_response = make_request(f"{api_url()}/exercises", headers={"Authorization": f"Bearer {token}"})
    assert protected_response["status"] == 200, "Protected endpoint should be accessible with valid token"


def test_authentication_failure():
    """Test that authentication fails with incorrect credentials."""
    wait_for_api()

    # Test login with incorrect credentials
    response = make_request(f"{api_url()}/login", method="POST", data={"username": "admin", "password": "wrongpassword"})
    assert response["status"] == 401, "Should return 401 for invalid credentials"

    # Verify that protected endpoint is not accessible without token
    protected_response = make_request(f"{api_url()}/exercises")
    assert protected_response["status"] == 401, "Protected endpoint should not be accessible without token"

from database.users import create_user
from controller.user import login_user

def test_login_user_success(db_session):
    """Test that login_user returns a token for valid credentials."""
    create_user(db_session, "testuser", "testpassword")
    result = login_user("testuser", "testpassword", db_session)
    assert result is not None


def test_login_user_failure(db_session):
    """Test that login_user returns None for invalid credentials."""
    create_user(db_session, "testuser", "testpassword")
    result = login_user("testuser", "wrongpassword", db_session)
    assert result is None
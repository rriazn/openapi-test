import os
import sys
from pathlib import Path
from typing import Generator

from fastapi.testclient import TestClient
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# API tests must run against the isolated test DB.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from auth_utils import get_token_for_user
from main import app
from database.db import get_db, reset_db
from database.users import create_user, get_user_by_username
from models import Routine, Exercise, User
from database.exercises import insert_exercise
from database.routines import insert_routine


@pytest.fixture(autouse=True)
def reset_database_between_tests() -> Generator[None, None, None]:
    # Ensure every test starts from a clean DB state.
    reset_db()
    yield
    # Defensive cleanup in case a test mutates DB after fixture setup.
    reset_db()


@pytest.fixture(autouse=True)
def prepare_api_test_db() -> None:
    """Reset test DB and ensure admin user exists before each API test."""
    reset_db()
    db = get_db()
    try:
        create_user(db, "admin", "password")
        user = get_user_by_username(db, "admin")
        assert user is not None
    finally:
        db.close()


@pytest.fixture()
def client():
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture(scope="function")
def random_string():
    import random
    import string

    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


@pytest.fixture()
def db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def user_credentials(random_string, db_session):
    username = f"user_{random_string}"
    password = "testpassword"
    create_user(db_session, username, password)
    return username, password


@pytest.fixture()
def user_instance(random_string, db_session):
    username = f"user_{random_string}"
    password = "testpassword"
    create_user(db_session, username, password)
    user = get_user_by_username(db_session, username)
    token = get_token_for_user(username)
    return user, token

    
@pytest.fixture()
def token(user_instance):
    return user_instance[1]


@pytest.fixture()
def exercise(random_string, db_session):
    exercise_name = f"exercise_{random_string}"
    exercise = Exercise(name=exercise_name, type="WR")
    inserted_exercise = insert_exercise(db_session, exercise)
    return inserted_exercise


@pytest.fixture()
def exercise_2(random_string, db_session):
    exercise_name = f"exercise_{random_string}_2"
    exercise = Exercise(name=exercise_name, type="WR")
    inserted_exercise = insert_exercise(db_session, exercise)
    return inserted_exercise


@pytest.fixture()
def routine(user_instance, exercise, db_session):
    routine_name = f"routine_{user_instance[0].username}_{exercise.name}"
    routine = Routine(name=routine_name, user_name=user_instance[0].username, exercises=[exercise])
    created_routine = insert_routine(db_session, routine)
    return created_routine


@pytest.fixture()
def routine_other_user(random_string, exercise, db_session):
    # Create a different user
    other_username = f"user_{random_string}_2"
    create_user(db_session, other_username, "testpassword")

    # Create a routine for the other user
    routine_name = f"routine_{other_username}_{exercise.name}"
    routine = Routine(name=routine_name, user_name=other_username, exercises=[exercise])
    created_routine = insert_routine(db_session, routine)
    return created_routine

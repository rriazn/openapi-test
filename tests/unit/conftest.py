import os
import sys
from pathlib import Path

import pytest
from typing import Generator
from sqlmodel import Session


# Make src/ importable when running plain `pytest` outside Hatch scripts.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# Unit tests always run against an isolated DB file.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from database.db import get_db
from database.db import reset_db
from database.exercises import insert_exercise
from database.routines import insert_routine
from models import Exercise, Routine


@pytest.fixture(autouse=True)
def reset_database_between_tests() -> Generator[None, None, None]:
    # Ensure every test starts from a clean DB state.
    reset_db()
    yield
    # Defensive cleanup in case a test mutates DB after fixture setup.
    reset_db()


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    db = get_db()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def random_string():
    import random
    import string

    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


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
def routine(random_string, exercise, db_session):
    routine_name = f"routine_{random_string}"
    routine = Routine(name=routine_name, user_name="admin", exercises=[exercise])
    inserted_routine = insert_routine(db_session, routine)
    return inserted_routine

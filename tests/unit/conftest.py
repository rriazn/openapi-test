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


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

from database.db import get_db


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    db = get_db()
    try:
        yield db
    finally:
        db.close()


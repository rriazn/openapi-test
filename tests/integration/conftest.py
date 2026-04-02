import os
import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_FILE = PROJECT_ROOT / "tests" / "integration" / "Users-test.csv"


@pytest.fixture(scope="session", autouse=True)
def preload_users_csv() -> None:
	"""Reset DB and import seed users before integration tests run."""
	env = os.environ.copy()
	env["DATABASE_URL"] = "sqlite:///./app.db"

	subprocess.run(
		["hatch", "run", "backend-cli", "reset-db"],
		cwd=PROJECT_ROOT,
		env=env,
		check=True,
	)
	subprocess.run(
		["hatch", "run", "backend-cli", "import-users", str(CSV_FILE)],
		cwd=PROJECT_ROOT,
		env=env,
		check=True,
	)

import subprocess
from models import ExerciseType


def test_reset_db(db_session):
    from cli import reset_db
    from database.users import get_all_users

    # Reset the database without creating a default user
    subprocess.Popen("hatch run backend-cli reset-db", shell=True).wait()

    # Verify that the database is empty
    users = get_all_users(db_session)
    assert len(users) == 0

def test_reset_db_create_user(db_session):
    from cli import reset_db
    from database.users import get_user_by_username

    # Reset the database and create a default user
    subprocess.Popen("hatch run backend-cli reset-db --create-default-user", shell=True).wait()

    # Verify that the default user was created
    user = get_user_by_username(db_session, "admin")
    assert user is not None
    assert user.username == "admin"

def test_add_exercise(db_session):
    from database.exercises import get_all_exercises

    # Add a new exercise
    subprocess.Popen("hatch run backend-cli add-exercise Push-up RO", shell=True).wait()

    # Verify that the exercise was added to the database
    exercises = get_all_exercises(db_session)
    assert len(exercises) == 1
    assert exercises[0].name == "Push-up"
    assert exercises[0].type == ExerciseType.RO
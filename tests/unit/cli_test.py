import subprocess
from models import ExerciseType


def test_reset_db(db_session):
    from database.users import get_all_users, create_user

    # Create a user to ensure the database is not empty
    create_user(db_session, "testuser", "testpassword")

    # Reset the database without creating a default user
    subprocess.Popen("hatch run backend-cli reset-db", shell=True).wait()

    # Verify that the database is empty
    users = get_all_users(db_session)
    assert len(users) == 0

def test_reset_db_create_user(db_session):
    from database.users import get_user_by_username

    # Reset the database and create a default user
    subprocess.Popen("hatch run backend-cli reset-db --create-default-user", shell=True).wait()

    # Verify that the default user was created
    user = get_user_by_username(db_session, "admin")
    assert user is not None
    assert user.username == "admin"

def test_import_users(db_session, tmp_path):
    from database.users import get_user_by_username

    # Create a temporary CSV file with user data
    csv_file = tmp_path / "users.csv"
    csv_file.write_text("username,password\nuser1,pass1\nuser2,pass2")

    # Import users from the CSV file
    subprocess.Popen(f"hatch run backend-cli import-users {csv_file}", shell=True).wait()

    # Verify that the users were imported into the database
    user1 = get_user_by_username(db_session, "user1")
    user2 = get_user_by_username(db_session, "user2")
    assert user1 is not None
    assert user1.username == "user1"
    assert user2 is not None
    assert user2.username == "user2"

def test_import_users_duplicate(db_session, tmp_path):
    from database.users import create_user, get_user_by_username

    # Create a user to cause a duplicate entry
    create_user(db_session, "user1", "pass1")
    # Create a temporary CSV file with duplicate user data
    csv_file = tmp_path / "users.csv"   
    csv_file.write_text("username,password\nuser1,pass1\nuser2,pass2")

    # Import users from the CSV file
    subprocess.Popen(f"hatch run backend-cli import-users {csv_file}", shell=True).wait()

    # Verify that the users were imported into the database
    user1 = get_user_by_username(db_session, "user1")
    user2 = get_user_by_username(db_session, "user2")
    assert user1 is not None
    assert user1.username == "user1"
    assert user2 is not None
    assert user2.username == "user2"


def test_add_exercise(db_session):
    from database.exercises import get_all_exercises

    # Add a new exercise
    subprocess.Popen("hatch run backend-cli add-exercise Push-up RO", shell=True).wait()

    # Verify that the exercise was added to the database
    exercises = get_all_exercises(db_session)
    assert len(exercises) == 1
    assert exercises[0].name == "Push-up"
    assert exercises[0].type == ExerciseType.RO

def test_import_exercises(db_session, tmp_path):
    from database.exercises import get_exercise_by_name

    # Create a temporary CSV file with exercise data
    csv_file = tmp_path / "exercises.csv"
    csv_file.write_text("name,type\nSquat,WR\nRunning,CA")

    # Import exercises from the CSV file
    subprocess.Popen(f"hatch run backend-cli import-exercises {csv_file}", shell=True).wait()

    # Verify that the exercises were imported into the database
    exercise1 = get_exercise_by_name(db_session, "Squat")
    exercise2 = get_exercise_by_name(db_session, "Running")
    assert exercise1 is not None
    assert exercise1.name == "Squat"
    assert exercise1.type == ExerciseType.WR
    assert exercise2 is not None
    assert exercise2.name == "Running"
    assert exercise2.type == ExerciseType.CA

def test_import_exercises_duplicate(db_session, tmp_path):
    from database.exercises import insert_exercise, get_exercise_by_name
    from models import Exercise

    # Add an exercise to cause a duplicate entry
    exercise = Exercise(name="Squat", type=ExerciseType.WR)
    insert_exercise(db_session, exercise)

    # Create a temporary CSV file with duplicate exercise data
    csv_file = tmp_path / "exercises.csv"
    csv_file.write_text("name,type\nSquat,WR\nRunning,CA")

    # Import exercises from the CSV file
    subprocess.Popen(f"hatch run backend-cli import-exercises {csv_file}", shell=True).wait()

    # Verify that the exercises were imported into the database
    exercise1 = get_exercise_by_name(db_session, "Squat")
    exercise2 = get_exercise_by_name(db_session, "Running")
    assert exercise1 is not None
    assert exercise1.name == "Squat"
    assert exercise1.type == ExerciseType.WR
    assert exercise2 is not None
    assert exercise2.name == "Running"
    assert exercise2.type == ExerciseType.CA

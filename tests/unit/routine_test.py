from controller.routines import update_routine


def test_update_routine_name(routine, db_session):
    updated_routine = update_routine(db_session, routine, "updated routine", [], [])
    assert updated_routine.name == "updated routine", "Routine name should be updated"


def test_update_routine_add_exercise(routine, exercise_2, db_session):
    updated_routine = update_routine(db_session, routine, "", [exercise_2], [])
    assert exercise_2 in updated_routine.exercises, "Exercise should be added to the routine"


def test_update_routine_remove_exercise(routine, exercise, db_session):
    updated_routine = update_routine(db_session, routine, "", [], [exercise])
    assert exercise not in updated_routine.exercises, "Exercise should be removed from the routine"
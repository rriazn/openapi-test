from sqlmodel import select
from models import Workout, WorkoutStatus


def create_workout(db, routine, date: str) -> int:
    workout = Workout(routine_id=routine.id, date=date, exercises=routine.exercises)
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def get_workout_by_id(db, workout_id: int) -> Workout:
    return db.exec(select(Workout).where(Workout.id == workout_id)).first()


def stop_workout_db(db, workout: Workout):
    workout.status = WorkoutStatus.STOPPED
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def update_workout_db(db, workout: Workout):
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout

from sqlmodel import Session, select

from models import Workout


def get_workouts_for_user(db: Session, username: str):
    return db.exec(select(Workout).where(Workout.user_name == username)).all()


def get_workout_by_id(db: Session, workout_id: int):
    return db.exec(select(Workout).where(Workout.id == workout_id)).first()


def insert_workout(db: Session, workout: Workout):
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


def remove_workout(db: Session, workout_id: int):
    try:
        workout = get_workout_by_id(db, workout_id)
        if workout:
            db.delete(workout)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e

from typing import Optional

from sqlmodel import Session, select

from models import Exercise


def get_all_exercises(db: Session) -> list[Exercise]:
    return db.exec(select(Exercise)).all()


def get_exercise_by_id(db: Session, exercise_id: int) -> Optional[Exercise]:
    return db.exec(select(Exercise).where(Exercise.id == exercise_id)).first()


def get_exercise_by_name(db: Session, name: str) -> Optional[Exercise]:
    return db.exec(select(Exercise).where(Exercise.name == name)).first()


def insert_exercise(db: Session, exercise: Exercise) -> Exercise:
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise
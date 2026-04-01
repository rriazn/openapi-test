from sqlmodel import Session, select

from models import Exercise


def get_all_exercises(db: Session) -> list[Exercise]:
    return db.exec(select(Exercise)).all()


def insert_exercise(db: Session, exercise: Exercise) -> Exercise:
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise
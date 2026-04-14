
from sqlmodel import Session, select

from models import Routine


def get_routines_for_user(db: Session, username: str):
    return db.exec(select(Routine).where(Routine.user_name == username)).all()


def get_routine_by_id(db: Session, routine_id: int):
    return db.exec(select(Routine).where(Routine.id == routine_id)).first()


def insert_routine(db: Session, routine: Routine):
    db.add(routine)
    db.commit()
    db.refresh(routine)
    return routine


def remove_routine(db: Session, routine_id: int):
    try:
        routine = get_routine_by_id(db, routine_id)
        if routine:
            db.delete(routine)
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    

def update_routine_db(db: Session, routine: Routine):
    try:
        db.add(routine)
        db.commit()
        db.refresh(routine)
    except Exception as e:
        db.rollback()
        raise e

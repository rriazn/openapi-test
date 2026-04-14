from typing import List
from sqlmodel import Session, select
from database.exercises import get_exercise_by_id
from database.routines import get_routine_by_id, update_routine_db
from models import Exercise, Routine


def update_routine(db: Session, routine: Routine, new_name: str, exercises_to_add: List[Exercise], exercises_to_remove: List[Exercise]):
    # Update routine name
    routine.name = new_name
    
    # Add new exercises
    for exercise in exercises_to_add:    
        if exercise not in routine.exercises:
            routine.exercises.append(exercise)
    
    # Remove exercises
    for exercise in exercises_to_remove:
        if exercise in routine.exercises:
            routine.exercises.remove(exercise)
    
    update_routine_db(db, routine)
    return routine
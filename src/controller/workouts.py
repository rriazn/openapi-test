from typing import List
from sqlmodel import Session
from database.workouts import update_workout_db
from models import Exercise, Workout


def update_workout_exercises(db: Session, workout: Workout, exercises_to_add: List[Exercise], exercises_to_remove: List[Exercise]):
    # Add new exercises
    for exercise in exercises_to_add:
        if exercise not in workout.exercises:
            workout.exercises.append(exercise)
    
    # Remove exercises
    for exercise in exercises_to_remove:
        if exercise in workout.exercises:
            workout.exercises.remove(exercise)
    
    update_workout_db(db, workout)
    return workout
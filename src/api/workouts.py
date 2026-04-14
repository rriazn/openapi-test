from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from datetime import datetime

from api.routines_specs import ActionResponse
from api.workouts_specs import WorkoutEditRequest, WorkoutStartResponse, WorkoutEditResponse
from auth_utils import get_username_from_token
from database.routines import get_routine_by_id
from database.workouts import create_workout, get_workout_by_id, stop_workout_db
from database.db import get_db
from controller.workouts import update_workout_exercises


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

@router.post("/workouts/{routine_id}/start", response_model=WorkoutStartResponse)
def start_workout(routine_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> WorkoutStartResponse:
    """Start a workout session."""

    # Check if the routine exists and belongs to the user
    username = get_username_from_token(token)
    routine = get_routine_by_id(db, routine_id)
    if not routine or routine.user_name != username:
        raise HTTPException(status_code=404, detail="Routine not found")
    
    # Create a new workout with the exercises from the routine
    try:
        workout = create_workout(db, routine, date=datetime.now().isoformat())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error starting workout: {str(e)}")
    return WorkoutStartResponse(workout=workout)


@router.post("/workouts/{workout_id}/stop")
def stop_workout(workout_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> ActionResponse:
    """Stop a workout session."""

    # Check if the workout exists and belongs to the user
    username = get_username_from_token(token)
    workout = get_workout_by_id(db, workout_id)
    if not workout or workout.routine.user_name != username:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout.status == "stopped":
        raise HTTPException(status_code=400, detail="Workout is already stopped")
    
    # Update workout status to stopped
    try:
        stop_workout_db(db, workout)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error stopping workout: {str(e)}")
    
    return ActionResponse(message="Workout stopped successfully")


@router.put("/workouts/{workout_id}/exercises")
def update_workout(workout_id: int, request: WorkoutEditRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Update exercises in an active workout session."""
    
    # Check if the workout exists and belongs to the user
    username = get_username_from_token(token)
    workout = get_workout_by_id(db, workout_id)
    if not workout or workout.routine.user_name != username:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout.status == "stopped":
        raise HTTPException(status_code=400, detail="Cannot update exercises in a stopped workout")
    
    # Update exercises in the workout
    try:
        workout = update_workout_exercises(db, workout, request.exercise_add, request.exercise_remove)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating workout exercises: {str(e)}")
    
    return WorkoutEditResponse(exercises=workout.exercises)

    
    
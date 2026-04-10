from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from api.workouts_specs import ActionResponse, WorkoutCreateResponse, WorkoutGetResponse, WorkoutCreateRequest, WorkoutDetailResponse, WorkoutGetListItem
from auth_utils import get_username_from_token
from database.db import get_db
from database.workouts import get_workouts_for_user, insert_workout, get_workout_by_id, remove_workout
from database.exercises import get_exercise_by_id
from models import Workout


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

@router.get("/workouts", response_model=WorkoutGetResponse)
def list_workouts(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """List all workouts for a user."""
    username = get_username_from_token(token)
    workouts = get_workouts_for_user(db, username)
    return WorkoutGetResponse(workouts=[WorkoutGetListItem(id=workout.id, name=workout.name) for workout in workouts])


@router.get("/workouts/{workout_id}", response_model=WorkoutDetailResponse)
def get_workout_detail(workout_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get details of a specific workout."""
    username = get_username_from_token(token)
    workout = get_workout_by_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout.user_name != username:
        raise HTTPException(status_code=403, detail="User is not the owner of this workout")
    return WorkoutDetailResponse(
        name=workout.name,
        owner=workout.user_name,
        exercises=[exercise.name for exercise in workout.exercises]
    )


@router.post("/workouts", response_model=WorkoutCreateResponse)
def create_workout(request: WorkoutCreateRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Create a new workout for the user."""
    username = get_username_from_token(token)
    exercises = []
    for exercise_id in request.exercise_ids:
        exercise = get_exercise_by_id(db, exercise_id)
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Exercise with id {exercise_id} not found")
        exercises.append(exercise)
    workout = Workout(
        name=request.workout_name, 
        user_name=username, 
        exercises=exercises
    )
    try:
        insert_workout(db, workout)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return WorkoutCreateResponse(
        id=workout.id,
        name=workout.name,
        owner=workout.user_name,
        exercises=[exercise.name for exercise in workout.exercises]
    )


@router.delete("/workouts/{workout_id}", response_model=ActionResponse)
def delete_workout(workout_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Delete a workout owned by the user."""
    username = get_username_from_token(token)
    workout = get_workout_by_id(db, workout_id)
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout.user_name != username:
        raise HTTPException(status_code=403, detail="User is not the owner of this workout")
    try:
        remove_workout(db, workout_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ActionResponse(message="Workout deleted successfully")
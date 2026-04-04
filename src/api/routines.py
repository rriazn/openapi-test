from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from api.routines_specs import ActionResponse, RoutineCreateResponse, RoutineGetResponse, RoutineCreateRequest, RoutineDetailResponse, RoutineGetListItem
from auth_utils import get_username_from_token
from database.db import get_db
from database.routines import get_routines_for_user, insert_routine, get_routine_by_id, remove_routine
from database.exercises import get_exercise_by_id
from models import Routine


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

@router.get("/routines", response_model=RoutineGetResponse)
def list_routines(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """List all routines for a user."""
    username = get_username_from_token(token)
    routines = get_routines_for_user(db, username)
    return RoutineGetResponse(routines=[RoutineGetListItem(id=routine.id, name=routine.name) for routine in routines])


@router.get("/routines/{routine_id}", response_model=RoutineDetailResponse)
def get_routine_detail(routine_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get details of a specific routine."""
    username = get_username_from_token(token)
    routine = get_routine_by_id(db, routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    if routine.user_name != username:
        raise HTTPException(status_code=403, detail="User is not the owner of this routine")
    return RoutineDetailResponse(
        name=routine.name,
        owner=routine.user_name,
        exercises=[exercise.name for exercise in routine.exercises]
    )


@router.post("/routines", response_model=RoutineCreateResponse)
def create_routine(request: RoutineCreateRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Create a new routine for the user."""
    username = get_username_from_token(token)
    exercises = []
    for exercise_id in request.exercise_ids:
        exercise = get_exercise_by_id(db, exercise_id)
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Exercise with id {exercise_id} not found")
        exercises.append(exercise)
    routine = Routine(
        name=request.routine_name, 
        user_name=username, 
        exercises=exercises
    )
    try:
        insert_routine(db, routine)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return RoutineCreateResponse(
        id=routine.id,
        name=routine.name,
        owner=routine.user_name,
        exercises=[exercise.name for exercise in routine.exercises]
    )


@router.delete("/routines/{routine_id}", response_model=ActionResponse)
def delete_routine(routine_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Delete a routine owned by the user."""
    username = get_username_from_token(token)
    routine = get_routine_by_id(db, routine_id)
    if not routine:
        raise HTTPException(status_code=404, detail="Routine not found")
    if routine.user_name != username:
        raise HTTPException(status_code=403, detail="User is not the owner of this routine")
    try:
        remove_routine(db, routine_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return ActionResponse(message="Routine deleted successfully")
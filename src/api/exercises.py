from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from api.exercises_specs import ExercisesGetResponse
from database.db import get_db
from database.exercises import get_all_exercises


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

@router.get("/exercises", response_model=ExercisesGetResponse)
def list_exercises(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """List all exercises in the database."""
    exercises = get_all_exercises(db)
    return ExercisesGetResponse(exercises=exercises)

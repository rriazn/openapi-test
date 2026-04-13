from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from database.db import get_db
from controller.user import login_user



router = APIRouter()


@router.post("/login")
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login endpoint that validates user credentials and returns an access token."""

    token = login_user(payload.username, payload.password, db)
    if token is not None:
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid username or password")
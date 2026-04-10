from database.users import get_user_by_username
from auth_utils import verify_password, get_token_for_user
from sqlmodel import Session

def login_user(username: str, password: str, db: Session) -> str | None:
    user = get_user_by_username(db, username)
    if user and verify_password(user.hashed_password, password):
        token = get_token_for_user(username)
        return token
    return None
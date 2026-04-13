from sqlmodel import Session, select
from typing import Optional
from auth_utils import hash_password
from models import User

def get_all_users(db: Session) -> list[User]:
    return db.exec(select(User)).all()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.exec(select(User).where(User.username == username)).first()


def create_user(db: Session, username: str, password: str) -> User:
    hashed_password = hash_password(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
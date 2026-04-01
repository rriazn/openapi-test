from argon2 import PasswordHasher
import jwt

ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except Exception:
        return False
    

def get_token_for_user(username: str) -> str:
    return jwt.encode({"sub": username}, "secret", algorithm="HS256")
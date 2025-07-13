from datetime import timedelta, datetime, timezone
from typing import Dict, Any

from jose import jwt
from passlib.context import CryptContext

from app.api.deps import db_dependency
from app.core.config import settings
from app.db.models import Users
from app.schemas.auth_schema import Token

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(
        username: str,
        user_id: int,
        role: str,
        expires_delta: timedelta,
        scope: str = "user"
) -> Token:
    """
    Creates a new JWT access token and encapsulate it in and Pydantic Token object,
    including expires_in
    """
    to_encode: Dict[str, Any] = {'sub': username, 'id': user_id, 'scope': scope, 'role': role}

    expires_at = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expires_at})

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    expires_in_seconds = int(expires_delta.total_seconds())

    return Token(
        access_token=encoded_jwt,
        token_type="bearer",
        expires_in=expires_in_seconds,
        scope=scope,
        message="Loging successful",
        role=role
    )


def authenticate_user(username: str, password: str, db: db_dependency):

    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user
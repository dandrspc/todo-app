import datetime
from datetime import timedelta, datetime, timezone
from typing import Annotated, Dict, Any, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(prefix='/auth', tags=["Auth"])

SECRET_KEY = '976fe2c34da4db6499952f8af0ade3106d96f9f1220e4758971526066a7863dd'
ALGORITHM = 'HS256'
EXPIRATION_TIME_IN_SECONDS = 3600

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    message: str
    role: str


class UserInDB(BaseModel):
    username: str
    user_id: int
    user_role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user


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

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    expires_in_seconds = int(expires_delta.total_seconds())

    return Token(
        access_token=encoded_jwt,
        token_type="bearer",
        expires_in=expires_in_seconds,
        scope=scope,
        message="Loging successful",
        role=role
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> UserInDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        return UserInDB(username=username, user_id=user_id, user_role=user_role)

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")


@router.post("", status_code=status.HTTP_200_OK)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

    return create_user_request


@router.post("/token", response_model=Token)
async def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                          db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    access_token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(seconds=EXPIRATION_TIME_IN_SECONDS)
    )
    print(access_token)
    return access_token

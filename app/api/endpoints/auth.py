from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.deps import db_dependency
from app.core.security import bcrypt_context, authenticate_user, create_access_token
from app.db.models import Users
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.schemas.auth_schema import Token, CreateUserRequest

router = APIRouter(prefix='/auth', tags=["Auth"])


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
        timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    )
    print(access_token)
    return access_token

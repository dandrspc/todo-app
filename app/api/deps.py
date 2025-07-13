from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from app.core.config import settings
from app.core.database import get_db

from app.schemas.user_schema import UserInDB

# --- Database Dependency ---
# This dependency provides a SQLAlchemy session to endpoints and other dependencies.
db_dependency = Annotated[Session, Depends(get_db)]

# --- OAuth2 Scheme for Token Extraction ---
# This tells FastAPI how to expect the token (Bearer token in the Authorization header)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


# --- OAuth2 Scheme for Token Extraction ---
# This tells FastAPI how to expect the token (Bearer token in the Authorization header)
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> UserInDB:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
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


user_dependency = Annotated[UserInDB, Depends(get_current_user)]

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from app.db.models import Todos
from app.core.database import SessionLocal
from .auth import get_current_user, UserInDB

router = APIRouter(prefix='/admin', tags=["Admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserInDB, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user.user_role != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')

    return db.query(Todos).all()


@router.delete('/todos/{todo_id}', status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def delete_todo_by_id(user: user_dependency, db: db_dependency, todo_id: str):
    # TODO: Implement
    if user.user_role != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')
    raise HTTPException(status_code=501, detail='Not implemented')

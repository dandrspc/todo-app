from fastapi import APIRouter, Depends, HTTPException, Path

from starlette import status
from app.api.deps import user_dependency, db_dependency
from app.db.models import Todos

router = APIRouter(prefix='/admin', tags=["Admin"])


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

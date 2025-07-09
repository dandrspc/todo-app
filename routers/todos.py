from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.params import Query
from pydantic import BaseModel, Field
from sqlalchemy import cast, Integer
from sqlalchemy.orm import Session
from starlette import status

from app.db.models import Todos
from app.core.database import SessionLocal
from .auth import get_current_user, UserInDB

router = APIRouter(prefix='/todos', tags=["Todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[UserInDB, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get('', status_code=status.HTTP_200_OK)
async def read_all(
        user: user_dependency,
        db: db_dependency,
        priority: int | None = Query(None, description="Filter Todos by priority", gt=0, lt=6),
        complete: bool | None = Query(None, description="Filter Todos by complete"),

        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(100, ge=1, description="Maximum number of items to return")
):
    query = db.query(Todos).filter(Todos.owner_id == user.user_id)

    if priority:
        query = query.filter(cast(Todos.priority, Integer) == priority)
    if complete is not None:
        query = query.filter(Todos.priority == priority)

    return query.offset(skip).limit(limit).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_by_id(
        user: user_dependency,
        db: db_dependency, todo_id: int = Path(gt=0)
):
    todo_model = (db.query(Todos).filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.user_id).first())
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("", response_model=TodoRequest, status_code=status.HTTP_200_OK)
async def create_todo(user: user_dependency,
                      db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.user_id)
    db.add(todo_model)
    db.commit()
    return todo_model


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    todo_model = (db.query(Todos)
                  .filter(Todos.owner_id == user.user_id)
                  .filter(Todos.id == todo_id)
                  .first())
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        user: user_dependency,
        db: db_dependency,
        todo_id: int = Path(gt=0)
):
    todo_model = (db.query(Todos)
                  .filter(Todos.owner_id == user.user_id)
                  .filter(Todos.id == todo_id)
                  .first())
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.query(Todos).filter(Todos.owner_id == user.user_id).filter(Todos.id == todo_id).delete()
    db.commit()

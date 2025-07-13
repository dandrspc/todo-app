from fastapi import APIRouter, HTTPException, Path
from fastapi.params import Query
from sqlalchemy import cast, Integer

from starlette import status

from app.api.deps import user_dependency, db_dependency
from app.db.models import Todos
from app.schemas.todo_schema import TodoCreate

router = APIRouter(prefix='/todos', tags=["Todos"])


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


@router.post("", response_model=TodoCreate, status_code=status.HTTP_200_OK)
async def create_todo(user: user_dependency,
                      db: db_dependency, todo_request: TodoCreate):
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.user_id)
    db.add(todo_model)
    db.commit()
    return todo_model


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency,
                      db: db_dependency,
                      todo_request: TodoCreate,
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

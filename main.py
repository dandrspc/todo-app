from fastapi import FastAPI

from app.db import models
from app.core.database import engine
from app.api.endpoints import auth, todos, admin

app = FastAPI(
    title="Todos API",
    version="0.1.0"
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)

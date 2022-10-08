from fastapi import FastAPI
from app.router import (
    base, task, auth
)
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# registry routers
app.include_router(base.router)
app.include_router(auth.router)
app.include_router(task.router)

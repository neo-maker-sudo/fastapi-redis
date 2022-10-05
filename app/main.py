from fastapi import FastAPI
from .router import task
from app.router import base, task

app = FastAPI()

app.include_router(base.router)
app.include_router(task.router)

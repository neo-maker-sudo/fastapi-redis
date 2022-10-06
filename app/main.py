from fastapi import FastAPI
from app.router import (
    base, task, auth
)

app = FastAPI()

# registry routers
app.include_router(base.router)
app.include_router(auth.router)
app.include_router(task.router)

from fastapi import FastAPI
from .router import task

app = FastAPI()

app.include_router(task)

@app.get("/")
def home_view():
    return {"Hello": "World"}
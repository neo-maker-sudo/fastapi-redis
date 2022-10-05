from pydantic import BaseModel

class TaskSchemaIn(BaseModel):
    name: str
    description: str

class TaskSchemaOut(BaseModel):
    name: str
    description: str
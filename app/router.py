from typing import List
from fastapi import APIRouter, status
from .schemas import TaskSchemaIn, TaskSchemaOut
from .models import Task

task = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)

@task.get("", response_model=List[TaskSchemaOut], status_code=status.HTTP_200_OK)
async def get_tasks_view():
    all_pks = Task.all_pks()
    return [Task.get(pk) for pk in all_pks]

@task.get("/{id}", response_model=TaskSchemaOut, status_code=status.HTTP_200_OK)
async def get_task_view(id: str):
    return Task.get(id)

@task.post("", response_model=TaskSchemaOut, status_code=status.HTTP_201_CREATED)
async def task_create_view(task: TaskSchemaIn):
    return Task(name=task.name, description=task.description).save()

@task.put("/{id}", response_model=TaskSchemaOut, status_code=status.HTTP_200_OK)
async def task_put_view(id: str, task: TaskSchemaIn):
    qs = Task.get(id)
    qs.name = task.name
    qs.description = task.description
    return qs.save()

@task.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def task_delete_view(id: str):
    return Task.delete(id)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Tasks(BaseModel):
    id: int
    title: str
    completed: bool

tasks_list = [

    Tasks(id=1, title="Buy Food", completed=False)
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    completed: bool


def generate_id():
    if tasks_list:
        return tasks_list[-1].id + 1
    
    return 1


@app.get("/tasks")
def get_tasks():
    return tasks_list

@app.post("/tasks")
def create_task(task: TaskCreate):
    new_task = Tasks(id=generate_id(), title=task.title, completed=False)
    tasks_list.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    for existing_task in tasks_list:
        if existing_task.id == task_id:
            existing_task.title = task.title
            existing_task.completed = task.completed
            return existing_task
    return {"error": "Task not found"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks_list:
        if task.id == task_id:
            tasks_list.remove(task)
            return {"message": "Task deleted successfully"}
    return {"error": "Task not found"}


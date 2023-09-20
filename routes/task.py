from fastapi import APIRouter, HTTPException
from database import get_all_tasks, create_task, get_one_task, get_one_task_id, delete_task, update_task
from model import Task, UpdateTask

task = APIRouter()

@task.get('/api/tasks')
async def get_tasks():
    tasks = await get_all_tasks()
    return tasks

@task.get('/api/tasks/{id}', response_model=Task)
async def get_task(id: int):
    return {"data": id}

@task.post('/api/tasks', response_model=Task)
async def save_task(task: Task):
    taskFound = await get_one_task(task.title)
    if taskFound:
        raise HTTPexception(409, 'Task already exists') 
        
    response = await create_task(task.dict())
    if response:
        return response
    raise HTTPexception(400, 'Something went wrong')
    
    return {"data": "Task created"}

@task.put('/api/tasks/{id}', response_model=Task)
async def put_task(id: str, task: UpdateTask):
    response = await update_task(id, task)
    if response:
        return response
    raise HTTPexception(404, f'Task with ID {id} not found!')


@task.delete('/api/tasks/{id}')
async def remove_task(id: int):
    response = await delete_task(id)
    if reponse:
        return 'Task successfully removed'
    raise HTTPexception(404, f'Task with ID {id} not found!')
    return {"data": f"Task {id} has been deleted"}
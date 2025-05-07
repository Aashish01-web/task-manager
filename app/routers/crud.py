from fastapi import APIRouter, HTTPException, Depends, status
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from models import Task

router = APIRouter(
    prefix='/crud',
    tags=['crud']
)

from .schema import GetTaskSchemaResponse, TaskCreateRequest

@router.get("/tasks/{task_id}", response_model=GetTaskSchemaResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by ID"""
    stmt = select(Task).filter(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.get("/tasks/", response_model=list[GetTaskSchemaResponse])
async def get_all_tasks(db: Session = Depends(get_db)):
    """Get all tasks"""
    stmt = select(Task)
    result = await db.execute(stmt)
    tasks = result.scalars().all()

    if tasks is None:
        raise HTTPException(status_code=404, detail="No task in tables!")

    return tasks

@router.post("/newTasks/", response_model=TaskCreateRequest)
async def create_task(task: TaskCreateRequest, db: Session = Depends(get_db)):
    """Create a new task"""
    try:
        db_task = Task(
            title=task.title,
            description=task.description,
            completed=task.completed,
        )

        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)

        return db_task
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}", response_model=TaskCreateRequest)
async def update_task(task_id: int, task: TaskCreateRequest, db: Session = Depends(get_db)):
    """Update a task by ID"""

    stmt = select(Task).filter(Task.id == task_id)
    result = await db.execute(stmt)
    existing_task = result.scalar_one_or_none()

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.completed = task.completed

    await db.commit()
    await db.refresh(existing_task)

    return existing_task

@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by ID"""
    stmt = select(Task).filter(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task)
    await db.commit()

    return {"detail": f"Task: {task_id} deleted successfully"}

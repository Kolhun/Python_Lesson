from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import List
from app_less_70_new.backends.bd_depends import get_db
from app_less_70_new.schemas import TaskResponse, TaskCreate, TaskUpdate
from app_less_70_new.models import Task, User

router = APIRouter(
    prefix="/task",
    tags=["task"]
)


@router.get("/", response_model=List[TaskResponse])
async def all_tasks(db: Session = Depends(get_db)):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get("/task/{task_id}", response_model=TaskResponse)
async def task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task:
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    new_task = Task(**task.dict(), user_id=user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    existing_task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if existing_task:
        db.execute(update(Task).where(Task.id == task_id).values(**task.dict()))
        db.commit()
        return db.query(Task).filter(Task.id == task_id).first()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.delete("/delete/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    existing_task = db.scalars(select(Task).where(Task.id == task_id)).first()
    if existing_task:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion is successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

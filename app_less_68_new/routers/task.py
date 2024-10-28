from fastapi import APIRouter

router = APIRouter(
    prefix="/task",
    tags=["task"]
)

@router.get("/")
async def all_tasks():
    return {"message": "All tasks"}

@router.get("/{task_id}")
async def task_by_id(task_id: int):
    return {"message": f"Task with id {task_id}"}

@router.post("/create")
async def create_task():
    return {"message": "Task created"}

@router.put("/update/{task_id}")
async def update_task(task_id: int):
    return {"message": f"Task with id {task_id} updated"}

@router.delete("/delete/{task_id}")
async def delete_task(task_id: int):
    return {"message": f"Task with id {task_id} deleted"}

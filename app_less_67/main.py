from fastapi import FastAPI
from .routers import task, user

app = FastAPI()

#uvicorn app_less_67.main:app --reload

@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}

# Подключение маршрутов
app.include_router(task.router)
app.include_router(user.router)



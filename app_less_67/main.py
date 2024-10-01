from fastapi import FastAPI
from .routers import tusk, user

#uvicorn app_less_67.main:app --reload


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}

# Подключение маршрутов
app.include_router(tusk.router)
app.include_router(user.router)

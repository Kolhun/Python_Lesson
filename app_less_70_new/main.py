from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from models import User, Task
from backends.bd import Base
from routers import task, user


#$env:PYTHONPATH="C:\VisualDevelop\Python_Lesson"
#alembic init app/migrations
#alembic revision --autogenerate -m "Initial migration"
#alembic upgrade head
#uvicorn main:app --reload

app = FastAPI()
engine = create_engine("sqlite:///taskmanager.db")

app.include_router(task.router)
app.include_router(user.router)

Base.metadata.create_all(bind=engine)

print(CreateTable(User.__table__).compile(engine))
print(CreateTable(Task.__table__).compile(engine))

@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}

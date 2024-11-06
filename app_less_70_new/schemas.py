from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class CreateUser(UserBase):
    pass

class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int

class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

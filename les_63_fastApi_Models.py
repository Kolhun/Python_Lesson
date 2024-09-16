from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users", response_model=List[User])
async def get_users():
    return users


@app.post("/user/{username}/{age}", response_model=User)
async def create_user(username: str, age: int):
    # Присваиваем ID, если список пустой, то id = 1, иначе увеличиваем на 1
    user_id = 1 if not users else users[-1].id + 1

    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)

    return new_user


@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: int, username: str, age: int):
    # Поиск пользователя по user_id
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int):
    # Поиск пользователя по user_id
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user

    raise HTTPException(status_code=404, detail="User was not found")

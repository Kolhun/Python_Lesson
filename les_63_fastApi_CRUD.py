from fastapi import FastAPI, HTTPException

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


# 1. GET запрос на получение всех пользователей
@app.get("/users")
async def get_users():
    return users


# 2. POST запрос для добавления нового пользователя
@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int):
    if not (5 <= len(username) <= 20) or not (18 <= age <= 120):
        raise HTTPException(status_code=400, detail="Invalid username or age")

    # Находим максимальный ключ в словаре и добавляем нового пользователя
    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"


# 3. PUT запрос для обновления пользователя
@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: str, username: str, age: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if not (5 <= len(username) <= 20) or not (18 <= age <= 120):
        raise HTTPException(status_code=400, detail="Invalid username or age")

    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {user_id} has been updated"


# 4. DELETE запрос для удаления пользователя
@app.delete("/user/{user_id}")
async def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return f"User {user_id} has been deleted"

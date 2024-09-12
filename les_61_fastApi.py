from fastapi import FastAPI

app = FastAPI()
#uvicorn les_61_fastApi:app --reload

@app.get("/")
def home():
    return "Главная страница"

@app.get("/user/admin")
def admin():
    return "Вы вошли как администратор"

@app.get("/user/{user_id}")
def user(user_id: int):
    return f"Вы вошли как пользователь № {user_id}"

@app.get("/user")
def user_info(username: str, age: int):
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"

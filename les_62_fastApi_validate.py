from fastapi import FastAPI, Path
from pydantic import BaseModel, Field, constr, conint
from typing import Annotated

app = FastAPI()

# Start: uvicorn les_62_fastApi_validate:app --reload
@app.get("/user/{user_id}")
async def get_user(
    user_id: Annotated[
        int,
        Path(..., description="Enter User ID", ge=1, le=100, example=1)
    ]
):
    return {"user_id": user_id}


@app.get("/user/{username}/{age}")
async def get_user_by_username_and_age(
    username: Annotated[
        constr(min_length=5, max_length=20),
        Path(..., description="Enter username", example="UrbanUser")
    ],
    age: Annotated[
        conint(ge=18, le=120),
        Path(..., description="Enter age", example=24)
    ]
):
    return {"username": username, "age": age}

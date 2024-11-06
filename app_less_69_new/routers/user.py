from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from typing import List

from app_less_69_new.backends.bd_depends import get_db
from app_less_69_new.schemas import CreateUser, UpdateUser, UserResponse
from app_less_69_new.models import User

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/", response_model=List[UserResponse])
async def all_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user/{user_id}", response_model=UserResponse)
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.scalars(select(User).where(User.id == user_id)).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_slug = slugify(user.username)
    new_user = User(**user.dict(), slug=user_slug)
    db.add(new_user)  # Используем db.add() вместо db.execute()
    db.commit()
    db.refresh(new_user)  # Чтобы обновить объект с актуальными данными (например, id)
    return new_user  # Возвращаем модель пользователя с актуальными данными


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user:
        db.execute(update(User).where(User.id == user_id).values(**user.dict()))
        db.commit()
        return db.query(User).filter(User.id == user_id).first()  # Возвращаем обновленный объект
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.scalars(select(User).where(User.id == user_id)).first()
    if existing_user:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

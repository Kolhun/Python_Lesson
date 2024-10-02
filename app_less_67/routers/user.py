from fastapi import APIRouter, HTTPException
from ..backends.bd import Database

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

db = Database()

class User:
    __tablename__ = 'les_67_users'

    def __init__(self, username, firstname, lastname, age, slug):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.slug = slug

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS les_67_users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                firstname VARCHAR(255),
                lastname VARCHAR(255),
                age INTEGER,
                slug VARCHAR(255) UNIQUE,
                CONSTRAINT unique_username UNIQUE (username)
            );
        """)

    def save(self, cursor):
        cursor.execute("""
            INSERT INTO les_67_users (username, firstname, lastname, age, slug)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (self.username, self.firstname, self.lastname, self.age, self.slug))
        return cursor.fetchone()[0]

@router.get("/")
async def all_users():
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_users")
        users = db.cursor.fetchall()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения пользователей: {e}")
    finally:
        db.close()

@router.get("/{user_id}")
async def user_by_id(user_id: int):
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_users WHERE id = %s", (user_id,))
        user = db.cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения пользователя: {e}")
    finally:
        db.close()

@router.post("/create")
async def create_user(username: str, firstname: str, lastname: str, age: int, slug: str):
    db.connect()
    try:
        new_user = User(username=username, firstname=firstname, lastname=lastname, age=age, slug=slug)
        user_id = new_user.save(db.cursor)
        db.connection.commit()
        return {"message": "User created", "user_id": user_id}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка создания пользователя: {e}")
    finally:
        db.close()

@router.put("/update/{user_id}")
async def update_user(user_id: int, firstname: str = None, lastname: str = None, age: int = None):
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_users WHERE id = %s", (user_id,))
        user = db.cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        update_fields = []
        update_values = []

        if firstname:
            update_fields.append("firstname = %s")
            update_values.append(firstname)
        if lastname:
            update_fields.append("lastname = %s")
            update_values.append(lastname)
        if age is not None:
            update_fields.append("age = %s")
            update_values.append(age)

        update_values.append(user_id)

        if update_fields:
            db.cursor.execute(
                f"UPDATE les_67_users SET {', '.join(update_fields)} WHERE id = %s",
                tuple(update_values)
            )
            db.connection.commit()
        return {"message": f"User with id {user_id} updated"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления пользователя: {e}")
    finally:
        db.close()

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_users WHERE id = %s", (user_id,))
        user = db.cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        db.cursor.execute("DELETE FROM les_67_users WHERE id = %s", (user_id,))
        db.connection.commit()
        return {"message": f"User with id {user_id} deleted"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка удаления пользователя: {e}")
    finally:
        db.close()

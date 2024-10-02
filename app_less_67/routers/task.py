from fastapi import APIRouter, HTTPException

from ..backends.bd import Database


router = APIRouter(
    prefix="/task",
    tags=["task"]
)

db = Database()

class Task:
    def __init__(self, title, content, priority=0, completed=False, user_id=None, slug=None):
        self.title = title
        self.content = content
        self.priority = priority
        self.completed = completed
        self.user_id = user_id
        self.slug = slug

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS les_67_tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT,
                priority INTEGER DEFAULT 0,
                completed BOOLEAN DEFAULT FALSE,
                user_id INTEGER NOT NULL,
                slug VARCHAR(255) UNIQUE,
                CONSTRAINT fk_user
                    FOREIGN KEY(user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE
            );
        """)

    def save(self, cursor):
        cursor.execute("""
            INSERT INTO les_67_tasks (title, content, priority, completed, user_id, slug)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (self.title, self.content, self.priority, self.completed, self.user_id, self.slug))

        return cursor.fetchone()[0]




@router.post("/create")
async def create_task(title: str, content: str, priority: int = 0, completed: bool = False, user_id: int = None, slug: str = None):
    db.connect()
    try:
        new_task = Task(title=title, content=content, priority=priority, completed=completed, user_id=user_id, slug=slug)
        db.cursor.execute(
            """
            INSERT INTO les_67_tasks (title, content, priority, completed, user_id, slug)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (new_task.title, new_task.content, new_task.priority, new_task.completed, new_task.user_id, new_task.slug)
        )
        task_id = db.cursor.fetchone()[0]
        db.connection.commit()
        return {"message": "Task created", "task_id": task_id}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка создания задачи: {e}")
    finally:
        db.close()

@router.get("/")
async def all_tasks():
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_tasks")
        tasks = db.cursor.fetchall()
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения задач: {e}")
    finally:
        db.close()

@router.get("/{task_id}")
async def task_by_id(task_id: int):
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_tasks WHERE id = %s", (task_id,))
        task = db.cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")
        return {"task": task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения задачи: {e}")
    finally:
        db.close()



@router.put("/update/{task_id}")
async def update_task(task_id: int, title: str = None, content: str = None, priority: int = None, completed: bool = None):
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_tasks WHERE id = %s", (task_id,))
        task = db.cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        # Обновляем поля, только если переданы новые значения
        update_fields = []
        update_values = []

        if title:
            update_fields.append("title = %s")
            update_values.append(title)
        if content:
            update_fields.append("content = %s")
            update_values.append(content)
        if priority is not None:
            update_fields.append("priority = %s")
            update_values.append(priority)
        if completed is not None:
            update_fields.append("completed = %s")
            update_values.append(completed)

        update_values.append(task_id)

        if update_fields:
            db.cursor.execute(
                f"UPDATE les_67_tasks SET {', '.join(update_fields)} WHERE id = %s",
                tuple(update_values)
            )
            db.connection.commit()
        return {"message": f"Task with id {task_id} updated"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка обновления задачи: {e}")
    finally:
        db.close()

@router.delete("/delete/{task_id}")
async def delete_task(task_id: int):
    db.connect()
    try:
        db.cursor.execute("SELECT * FROM les_67_tasks WHERE id = %s", (task_id,))
        task = db.cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        db.cursor.execute("DELETE FROM les_67_tasks WHERE id = %s", (task_id,))
        db.connection.commit()
        return {"message": f"Task with id {task_id} deleted"}
    except Exception as e:
        db.connection.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка удаления задачи: {e}")
    finally:
        db.close()

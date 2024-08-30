import random

import psycopg2
import os

db_params = {
    'dbname': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'root'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

try:
    conn = psycopg2.connect(**db_params)
    print("Подключение установлено успешно!")
except psycopg2.Error as e:
    print(f"Ошибка подключения: {e}")
    exit(1)

cur = conn.cursor()

try:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "USER_ADMIN" (
            id INTEGER,
            username TEXT,
            first_name TEXT,
            block INTEGER
        )
    """)
    print("Таблица создана успешно!")
except psycopg2.Error as e:
    print(f"Ошибка выполнения запроса: {e}")


def user_add(user_id, username, first_name):
    check_user = cur.execute("""SELECT * FROM "USER_ADMIN" WHERE id != %s""", (user_id,))
    if check_user.fetchone() is None:
        cur.execute(f"INSERT INTO \"USER_ADMIN\" VALUES ({user_id},{username},{first_name},0)", (user_id,))
        conn.commit()


conn.commit()
cur.close()
conn.close()
print("Соединение с базой данных закрыто.")

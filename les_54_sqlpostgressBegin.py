from random import random
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
        CREATE TABLE IF NOT EXISTS "USER" (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER
        )
    """)
    print("Таблица создана успешно!")
except psycopg2.Error as e:
    print(f"Ошибка выполнения запроса: {e}")
for i in range(30):
    cur.execute("""
            insert into "USER" (username, email, age) values (%s, %s, %s)
    """, (f"newuser_{i}", f"sdfsd_{i}@mail.ru", str(random.randint(18, 50))))
cur.execute("""UPDATE "USER" SET age = %s WHERE username = %s""", (28, "newuser_12"))
conn.commit()
cur.close()
conn.close()
print("Соединение с базой данных закрыто.")

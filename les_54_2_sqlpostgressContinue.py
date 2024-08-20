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
        CREATE TABLE IF NOT EXISTS "USER_LESSON" (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            balance INTEGER NOT NULL
        )
    """)
    print("Таблица создана успешно!")
except psycopg2.Error as e:
    print(f"Ошибка выполнения запроса: {e}")
# for i in range(30):
#     cur.execute("""
#             insert into "USER" (username, email, age) values (%s, %s, %s)
#     """, (f"newuser_{i}", f"sdfsd_{i}@mail.ru", str(random.randint(18, 50))))
for i in range(10):
    username = f"User{i}"
    email = f"example{i}@gmail.com"
    age = random.randint(18, 50)
    balance = 1000

    cur.execute("""
        INSERT INTO "USER_LESSON" (username, email, age, balance)
        SELECT %s, %s, %s, %s
        WHERE NOT EXISTS (
            SELECT 1 FROM "USER_LESSON" WHERE username = %s
        )
    """, (username, email, age, balance, username))

cur.execute("""
    UPDATE "USER_LESSON"
    SET balance = 500
    WHERE id % 2 = 1
""")
conn.commit()
cur.execute("""
    DELETE FROM "USER_LESSON"
    WHERE id IN (SELECT id FROM "USER_LESSON" WHERE id % 3 = 1)
""")
conn.commit()
cur.execute("""
    SELECT username, email, age, balance
    FROM "USER_LESSON"
    WHERE age != 60
""")
conn.commit()
users = cur.fetchall()

for user in users:
    print(f"Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}")
# Show in console
# Подключение установлено успешно!
# Таблица создана успешно!
# Имя: User1 | Почта: example1@gmail.com | Возраст: 24 | Баланс: 500
# Имя: User5 | Почта: example5@gmail.com | Возраст: 18 | Баланс: 500
# Имя: User7 | Почта: example7@gmail.com | Возраст: 48 | Баланс: 500
# Имя: User3 | Почта: example3@gmail.com | Возраст: 35 | Баланс: 1000
# Имя: User9 | Почта: example9@gmail.com | Возраст: 29 | Баланс: 1000
# Имя: User2 | Почта: example2@gmail.com | Возраст: 24 | Баланс: 500
# Имя: User4 | Почта: example4@gmail.com | Возраст: 20 | Баланс: 500
# Имя: User8 | Почта: example8@gmail.com | Возраст: 37 | Баланс: 500
# Имя: User0 | Почта: example0@gmail.com | Возраст: 34 | Баланс: 500
# Соединение с базой данных закрыто.
#
# Process finished with exit code 0


cur.close()
conn.close()
print("Соединение с базой данных закрыто.")

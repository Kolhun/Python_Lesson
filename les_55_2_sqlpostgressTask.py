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

cur.execute("""SELECT SUM(balance) FROM "USER_LESSON" """)
data_sum_balance = cur.fetchone()[0]
print(f"Сумма всех балансов: {data_sum_balance}")
conn.commit()
cur.execute("""DELETE FROM "USER_LESSON" WHERE id = %s""", (6,))
conn.commit()
cur.execute("""SELECT COUNT(*) FROM "USER_LESSON" """)
data_sum_id = cur.fetchone()[0]
print(f"Общее колличество записей: {data_sum_id}")
conn.commit()
cur.execute("""SELECT AVG(balance) FROM "USER_LESSON" """)
data_avg = cur.fetchone()[0]
print(f"Средний баланс всех пользователей: {data_avg}")
conn.commit()

# Show in console
# Подключение установлено успешно!
# Таблица создана успешно!
# Сумма всех балансов: 6000
# Общее колличество записей: 10
# Средний баланс всех пользователей: 600.0000000000000000
# Соединение с базой данных закрыто.
#
# Process finished with exit code 0


cur.close()
conn.close()
print("Соединение с базой данных закрыто.")

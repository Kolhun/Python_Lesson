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

cur.execute("""SELECT COUNT(*) FROM "USER" WHERE age>20""")

# users = cur.fetchall()
# for user in users:
#     print(f"Пользователь: {user}")

total1 = cur.fetchone()[0]
total2 = cur.fetchall()

conn.commit()
cur.close()
conn.close()
print("Соединение с базой данных закрыто.")

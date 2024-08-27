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

#cur.execute("""SELECT COUNT(*) FROM "USER" WHERE age>20""")
# total1 = cur.fetchone()[0]
# total2 = cur.fetchall()
# print(total1)
# print(total2)

# cur.execute("""SELECT SUM(age) FROM "USER" """)
# total_first_sum = cur.fetchone()[0]
# cur.execute("""SELECT COUNT(*) FROM "USER" """)
# total_second_sum = cur.fetchone()[0]
# print(total_first_sum/total_second_sum)

cur.execute("""SELECT MAX(age) FROM "USER" """)
total_data = cur.fetchone()[0]
print(total_data)

# users = cur.fetchall()
# for user in users:
#     print(f"Пользователь: {user}")


conn.commit()
cur.close()
conn.close()
print("Соединение с базой данных закрыто.")

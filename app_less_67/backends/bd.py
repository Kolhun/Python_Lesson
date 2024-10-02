import os
import psycopg2
from psycopg2 import sql

db_params = {
    'dbname': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'root'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Подключение к базе данных"""
        try:
            self.connection = psycopg2.connect(**db_params)
            self.cursor = self.connection.cursor()
            print("Успешное подключение к базе данных")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def close(self):
        """Закрытие подключения к базе данных"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")

# Пример использования
if __name__ == "__main__":
    db = Database()
    db.connect()
    db.close()

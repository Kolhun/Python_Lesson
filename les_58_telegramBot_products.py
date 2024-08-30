import asyncio
import logging
import random
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile

import config
import asyncpg
import os

db_params = {
    'dbname': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'admin'),
    'password': os.getenv('POSTGRES_PASSWORD', 'root'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

def create_dsn(params):
    return f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}"

async def initiate_db(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                price INTEGER NOT NULL
            );
        """)

async def get_all_products(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        return await connection.fetch("SELECT * FROM Products;")

async def populate_products(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        products = [
            ('Продукт 1', 'Описание продукта 1', 100),
            ('Продукт 2', 'Описание продукта 2', 200),
            ('Продукт 3', 'Описание продукта 3', 300),
            ('Продукт 4', 'Описание продукта 4', 400),
        ]

        # Проверяем наличие каждого продукта и добавляем только если его нет в базе
        for title, description, price in products:
            await connection.execute("""
                INSERT INTO Products (title, description, price)
                SELECT $1, $2, $3
                WHERE NOT EXISTS (
                    SELECT 1 FROM Products WHERE title = $1
                )
            """, title, description, price)
        
        

async def create_pool():
    dsn = create_dsn(db_params)
    return await asyncpg.create_pool(dsn)

api = config.TOKEN
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def on_startup(dp: Dispatcher):
    pool = await create_pool()
    await initiate_db(pool)
    await populate_products(pool)  # Заполняем таблицу продуктами
    dp['db_pool'] = pool
    print("База данных инициализирована, продукты добавлены.")

@dp.message(Command("start"))
async def start_message(message: Message):
    await message.answer("Запускаемся ;D", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>!", parse_mode="HTML")

@dp.message(Command("products"))
async def list_products(message: Message):
    pool = dp['db_pool']
    products = await get_all_products(pool)

    if not products:
        await message.answer("В данный момент нет доступных продуктов.")
        return

    response = "Доступные продукты:\n\n"
    for product in products:
        response += f"Название: {product['title']} | Описание: {product['description']} | Цена: {product['price']}\n"

    await message.answer(response)

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
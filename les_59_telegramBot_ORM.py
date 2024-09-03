import asyncio
import logging
import random
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext

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

def create_db_url(params):
    """Создать строку подключения для PostgreSQL."""
    return f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}"

db_url = create_db_url(db_params)

async def initiate_db():
    conn = await asyncpg.connect(db_url)
    await conn.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL DEFAULT 1000
    )
    ''')
    await conn.close()

async def add_user(username, email, age):
    conn = await asyncpg.connect(db_url)
    await conn.execute('''
    INSERT INTO Users (username, email, age, balance)
    VALUES ($1, $2, $3, $4)
    ''', username, email, age, 1000)
    await conn.close()

async def is_included(username):
    """Проверка, есть ли пользователь в таблице Users."""
    conn = await asyncpg.connect(db_url)
    result = await conn.fetchval('''
    SELECT EXISTS(SELECT 1 FROM Users WHERE username = $1)
    ''', username)
    await conn.close()
    return result


API_TOKEN = config.TOKEN

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Инициализация базы данных
async def on_startup(dispatcher):
    await initiate_db()

main_menu = ReplyKeyboardBuilder()

main_menu.button(text="Регистрация")
main_menu_markup = main_menu.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Добро пожаловать! Выберите действие:", reply_markup=main_menu_markup)

# Классы состояний и обработка регистрации
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()

@dp.message(F.text == "Регистрация")
async def sing_up(message: types.Message, state: FSMContext):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)

@dp.message(RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    if not username.isalpha():
        await message.reply("Имя пользователя должно содержать только латинские буквы.")
        return

    if await is_included(username):
        await message.reply("Пользователь существует, введите другое имя.")
    else:
        await state.update_data(username=username)
        await message.reply("Введите свой email:")
        await state.set_state(RegistrationState.email)

@dp.message(RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text.strip()
    await state.update_data(email=email)
    await message.reply("Введите свой возраст:")
    await state.set_state(RegistrationState.age)

@dp.message(RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age_text = message.text.strip()
    if not age_text.isdigit():
        await message.reply("Возраст должен быть числом.")
        return

    age = int(age_text)
    user_data = await state.get_data()
    username = user_data['username']
    email = user_data['email']

    await add_user(username, email, age)
    await message.reply(f"Регистрация завершена! Ваш баланс: 1000")
    await state.clear()

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
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

products = []


def create_dsn(params):
    return f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}"


async def initiate_db(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                price INTEGER NOT NULL,
                img_path TEXT
            );
        """)


async def get_all_products(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        return await connection.fetch("SELECT * FROM Products;")


async def populate_products(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        products = [
            ('Продукт 1', 'Описание продукта 1', 100, "img_price_1.png"),
            ('Продукт 2', 'Описание продукта 2', 200, "img_price_2.png"),
            ('Продукт 3', 'Описание продукта 3', 300, "img_price_3.png"),
            ('Продукт 4', 'Описание продукта 4', 400, "img_price_4.png"),
            ('Продукт 5', 'Описание продукта 5', 500, "img_price_5.png")
        ]

        for title, description, price, img_path in products:
            await connection.execute("""
                INSERT INTO Products (title, description, price, img_path)
                SELECT $1, $2, $3, $4
                WHERE NOT EXISTS (
                    SELECT 1 FROM Products WHERE title = $1
                )
            """, title, description, price, img_path)


start_kb = ReplyKeyboardBuilder()
start_kb.button(text="Рассчитать")
start_kb.button(text="О нас")
start_kb.button(text="Купить")
start_kb.adjust(2)
start_markup = start_kb.as_markup(resize_keyboard=True)


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
    await populate_products(pool)
    dp['db_pool'] = pool
    print("База данных инициализирована, продукты добавлены.")


@dp.message(Command("start"))
async def start_message(message: Message):
    await message.answer("Запускаемся ;D", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>!", parse_mode="HTML", reply_markup=start_markup)


@dp.message(F.text == "Рассчитать")
async def about_message(message: Message, state: FSMContext):
    await message.answer("Как тебя зовут?")
    await state.set_state(UserState.name)


@dp.message(F.text == "О нас")
async def about_message(message: Message):
    await message.answer("Пункт меню о нас", reply_markup=start_markup)


class UserState(StatesGroup):
    name = State()
    age = State()
    growth = State()
    weight = State()
    calories = State()


@dp.message(F.text == "Купить")
async def list_products(message: Message):
    pool = dp['db_pool']
    products = await get_all_products(pool)

    if not products:
        await message.answer("В данный момент нет доступных продуктов.")
        return

    kb = InlineKeyboardBuilder()

    for product in products:
        title = product['title']
        description = product['description']
        price = product['price']
        img_path = product['img_path']

        response = f"<b>Название:</b> {title}\n<b>Описание:</b> {description}\n<b>Цена:</b> {price} ₽"

        try:
            photo = FSInputFile(img_path)
            await message.answer_photo(photo=photo, caption=response, parse_mode="HTML")
        except FileNotFoundError:
            await message.answer(f"Изображение для {title} не найдено.\n\n{response}")

        kb.add(InlineKeyboardButton(text=f"Купить {title}", callback_data=title))

    kb.adjust(len(products))
    await message.answer("Выберите товар для покупки:", reply_markup=kb.as_markup())


@dp.callback_query()
async def handle_product_purchase(callback: CallbackQuery):
    await callback.message.answer(f"Товар '{callback.data}' успешно куплен!")
    await callback.answer()


@dp.message(UserState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Какой твой рост?")
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def process_growth(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Какой твой вес?")
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    user_data = await state.get_data()
    age = int(user_data['age'])
    growth = int(user_data['growth'])
    weight = int(user_data['weight'])
    bmr = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(
        f"Тебя зовут {user_data['name']} и Вам {user_data['age']} год, твой рост {user_data['growth']} см и весишь ты {user_data['weight']} кг, твоя норма колорий - {bmr} кк (ну ты и обжора)")
    await state.clear()


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

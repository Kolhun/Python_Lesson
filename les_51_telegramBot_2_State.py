from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
import asyncio
import logging
import sys
import config_private as config

api = config.TOKEN
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class UserState(StatesGroup):
    name = State()
    age = State()
    growth = State()
    weight = State()
    calories = State()


@dp.message(Command(commands=["start"]))
async def start_message(message: Message, state: FSMContext):
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! Я бот помогающий твоему здоровью",
                         parse_mode="HTML")
    await message.answer("Как тебя зовут?")
    await state.set_state(UserState.name)


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


# @dp.message()
# async def all_message(message: types.Message):
#     await message.answer("Введите команду /start, чтобы начать общение")


async def on_startup():
    print("Bot is online!")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

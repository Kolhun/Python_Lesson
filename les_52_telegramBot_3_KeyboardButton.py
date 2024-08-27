from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery
import asyncio
import logging
import sys
import config

api = config.TOKEN
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! Я бот, помогающий твоему здоровью",
                         parse_mode="HTML")
    inline_kb = InlineKeyboardBuilder()
    inline_kb.button(text="Нажми меня", callback_data="button_pressed")
    inline_kb.adjust(1)

    await message.answer("Привет! Вот твоя кнопка:", reply_markup=inline_kb.as_markup())


@dp.callback_query(F.data == "button_pressed")
async def callback_button_pressed(callback_query: CallbackQuery):
    await callback_query.answer("Кнопка была нажата!")


@dp.message(Command("menu"))
async def menu_handler(message: types.Message):
    reply_kb = ReplyKeyboardBuilder()
    reply_kb.button(text="Рассчитать")
    reply_kb.button(text="Информация")
    reply_kb.adjust(2)

    await message.answer("Выберите опцию:", reply_markup=reply_kb.as_markup(resize_keyboard=True))


@dp.message(F.text == "Рассчитать")
async def check_message(message: types.Message, state: FSMContext):
    # if message.text == "Информация":
    #     await message.answer("Информация о боте")
    # elif message.text == "Рассчитать":
    #     await message.answer("Сколько тебе лет?")
    #     await state.set_state(UserState.age)
    await state.set_state(UserState.age)
    await message.answer("Сколько тебе лет?")


@dp.message(F.text == "Информация")
async def check_message(message: types.Message, state: FSMContext):
    await message.answer("Информация о боте")


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
        f"Привет! Тебе {user_data['age']} год, твой рост {user_data['growth']} см и весишь ты {user_data['weight']} кг, твоя норма калорий - {bmr} ккал.")
    await state.clear()


async def on_startup():
    print("Bot is online!")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, Message
from aiogram import F
import asyncio
import logging
import sys
import config as config

api = config.TOKEN
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

def calculate_menu_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def main_menu_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Рассчитать", callback_data="calculate")],
        [InlineKeyboardButton(text="Информация", callback_data="info")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

@dp.message(Command("start"))
async def start_message(message: types.Message):
    await message.answer("Запуск меню...", reply_markup=ReplyKeyboardRemove())
    await message.answer("Выберите опцию:", reply_markup=main_menu_kb())

@dp.callback_query(F.data == "calculate")
async def main_menu(call: types.CallbackQuery):
    await call.message.edit_text("Выберите опцию:", reply_markup=calculate_menu_kb())
    await call.answer()

@dp.callback_query(F.data == "info")
async def main_menu(message: types.Message):
    await message.answer("Информация о боте")

@dp.callback_query(F.data == "formulas")
async def get_formulas(call: types.CallbackQuery):
    formula_message = (
        "Формула Миффлина-Сан Жеора для расчёта базального уровня метаболизма:\n"
        "Для мужчин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n"
        "Для женщин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    )
    await call.message.answer(formula_message)
    await call.answer()

@dp.callback_query(F.data == "calories")
async def set_age(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите ваш возраст:")
    await call.answer()
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
        f"Привет! Тебе {user_data['age']} год, твой рост {user_data['growth']} см и весишь ты {user_data['weight']} кг, твоя норма колорий - {bmr} кк (ну ты и обжора)")
    await state.clear()

async def on_startup():
    print("Бот запущен!")

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
import asyncio
import logging
import sys
import config_private as config

# Токен вашего бота из конфигурационного файла
api = config.TOKEN
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# Создание инлайн-клавиатуры для меню "Рассчитать"
def calculate_menu_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")],
        [InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


# Создание основного меню
def main_menu_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Рассчитать", callback_data="calculate")],
        [InlineKeyboardButton(text="Информация", callback_data="info")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)



# Обработчик команды /start
@dp.message(Command("start"))
async def start_message(message: types.Message):
    # Отправляем основное меню
    await message.answer("Выберите опцию:", reply_markup=main_menu_kb())


# Обработчик нажатия на кнопку "Рассчитать"
@dp.callback_query(F.data == "calculate")
async def main_menu(call: types.CallbackQuery):
    # Отправляем меню с опциями расчёта
    await call.message.edit_text("Выберите опцию:", reply_markup=calculate_menu_kb())
    await call.answer()


@dp.callback_query(F.data == "info")
async def main_menu(message: types.Message):
    await message.answer("Информация о боте")


# Обработчик нажатия на кнопку "Формулы расчёта"
@dp.callback_query(F.data == "formulas")
async def get_formulas(call: types.CallbackQuery):
    # Отправляем формулу Миффлина-Сан Жеора
    formula_message = (
        "Формула Миффлина-Сан Жеора для расчёта базального уровня метаболизма:\n"
        "Для мужчин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5\n"
        "Для женщин: BMR = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) - 161"
    )
    await call.message.answer(formula_message)
    await call.answer()


# Обработчик нажатия на кнопку "Рассчитать норму калорий"
@dp.callback_query(F.data == "calories")
async def set_age(call: types.CallbackQuery):
    # Здесь можно начать машину состояний для расчёта калорий
    # Например, попросить пользователя ввести возраст, вес и рост
    await call.message.answer("Введите ваш возраст:")
    await call.answer()


# Функция для запуска бота
async def on_startup():
    print("Бот запущен!")


async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile

import config
import les_56_3_telegramBot_texts_board_game_sales as botTexts
import les_56_2_telegramBot_keyboards_board_game_sales as botKeyboards

api = config.TOKEN
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def start_message(message: Message):
    await message.answer("Запускаемся ;D", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! {botTexts.message_start}",
                         parse_mode="HTML", reply_markup=botKeyboards.start_markup)


@dp.message(F.text == "О нас")
async def about_message(message: Message):
    photo = FSInputFile("phone.jpg")
    # await message.answer_photo(photo, botTexts.message_about, reply_markup=botKeyboards.start_markup)
    await message.answer(botTexts.message_about, reply_markup=botKeyboards.start_markup)


@dp.message(F.text == "Стоимость")
async def message_price(message: Message):
    await message.answer("Что желаете посмотреть?", reply_markup=botKeyboards.catalog_markup)


@dp.callback_query(F.data == "medium")
async def message_medium(call: types.CallbackQuery):
    await call.message.answer(botTexts.message_game_M, reply_markup=botKeyboards.buy_markup)


@dp.callback_query(F.data == "large")
async def message_large(call: types.CallbackQuery):
    await call.message.answer(botTexts.message_game_L, reply_markup=botKeyboards.buy_markup)


@dp.callback_query(F.data == "superlarge")
async def message_superlarge(call: types.CallbackQuery):
    await call.message.answer(botTexts.message_game_XL, reply_markup=botKeyboards.buy_markup)


@dp.callback_query(F.data == "behinde")
async def message_behinde(call: types.CallbackQuery):
    await call.message.answer(botTexts.message_behinde, reply_markup=botKeyboards.catalog_markup)


@dp.callback_query(F.data == "buy")
async def message_buy(call: types.CallbackQuery):
    try:
        await call.message.edit_text("Благодарим за покупку!")
        await call.message.edit_reply_markup()
        await call.answer()
    except Exception as e:
        print(f"Error occurred: {e}")


async def on_startup():
    print("Bot is online!")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

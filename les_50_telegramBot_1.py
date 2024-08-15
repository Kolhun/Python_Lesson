from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import Message
import asyncio
import logging
import sys
import config_private as config

api = config.TOKEN
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(CommandStart())
async def start_message(message: Message):
    await message.answer(f"Привет, <b>{message.from_user.full_name}</b>! Я бот помогающий твоему здоровью", parse_mode="HTML")


@dp.message()
async def all_message(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение")


async def on_startup():
    print("Bot is online!")


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

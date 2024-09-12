import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from transformers import pipeline
from aiogram import F

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
API_TOKEN = '6941489417:AAFiNIiGfIXfAmNl3sSb00cXTTNzVfDuf44'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация NLP модели (предобученная DialoGPT)
nlp = pipeline('text-generation', model="microsoft/DialoGPT-medium")

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("Привет! Я чат-бот, задавай мне вопросы.")

# Обработка текстовых сообщений
@dp.message(F.text)
async def handle_message(message: Message):
    user_input = message.text
    response = nlp(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']
    await message.answer(response)

# Основная функция запуска бота
async def main():
    # Пропуск всех предыдущих апдейтов при запуске
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

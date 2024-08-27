from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

start_kb = ReplyKeyboardBuilder()

start_kb.button(text="Стоимость")
start_kb.button(text="О нас")
start_kb.adjust(2)
start_markup = start_kb.as_markup(resize_keyboard=True)

from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

start_kb = ReplyKeyboardBuilder()

start_kb.button(text="Стоимость")
start_kb.button(text="О нас")
start_kb.adjust(2)
start_markup = start_kb.as_markup(resize_keyboard=True)

catalog_kb = InlineKeyboardBuilder()
catalog_kb.row(InlineKeyboardButton(text="Средняя игра", callback_data="medium"))
catalog_kb.row(InlineKeyboardButton(text="Большая игра", callback_data="large"))
catalog_kb.row(InlineKeyboardButton(text="Огромная игра", callback_data="superlarge"))
catalog_kb.row(InlineKeyboardButton(text="Другие предложения", callback_data="behinde"))
catalog_markup = catalog_kb.as_markup()


buy_kb = InlineKeyboardBuilder()
buy_kb.row(InlineKeyboardButton(text="Купить!", callback_data="buy"))
buy_markup = buy_kb.as_markup()


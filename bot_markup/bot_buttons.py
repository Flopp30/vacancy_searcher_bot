from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

paginator_markup = InlineKeyboardMarkup(row_width=2)

btn_prev = InlineKeyboardButton(text='<<', callback_data="prev")
btn_next = InlineKeyboardButton(text='>>', callback_data="next")

paginator_markup.insert(btn_prev)
paginator_markup.insert(btn_next)

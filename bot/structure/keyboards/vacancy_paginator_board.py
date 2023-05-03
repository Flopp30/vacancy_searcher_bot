"""
Paginator keyboard
"""
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.structure import SearchCallBack

builder = InlineKeyboardBuilder()

builder.button(
    text="<<", callback_data=SearchCallBack(direction="prev")
)
builder.button(
    text=">>", callback_data=SearchCallBack(direction="next")
)

PAGINATOR_BOARD = builder.as_markup()

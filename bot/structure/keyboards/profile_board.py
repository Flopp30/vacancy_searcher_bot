from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.structure import ProfileCallback

builder = InlineKeyboardBuilder()
builder.button(
    text="Посмотреть вакансии", callback_data=ProfileCallback(action="search")
)
builder.adjust(1)

PROFILE_BOARD = builder.as_markup()

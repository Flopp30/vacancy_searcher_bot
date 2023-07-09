from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.structure import ProfileCallback, ProfileCDAction

builder = InlineKeyboardBuilder()
builder.button(
    text="Посмотреть вакансии", callback_data=ProfileCallback(action=ProfileCDAction.SHOW_VACANCIES)
)
builder.adjust(1)

PROFILE_BOARD = builder.as_markup()

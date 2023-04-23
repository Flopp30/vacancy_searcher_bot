from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

from bot.bot_messages import TEXT_GREETING


async def start(message: types.Message) -> None:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.row(
        KeyboardButton(text="Поиск по вакансиям"),
        KeyboardButton(text="Расширенный поиск"),
    )
    menu_builder.row(
        KeyboardButton(text="Профиль"),
        KeyboardButton(text="Помощь"),
    )

    await message.answer(
        TEXT_GREETING,
        reply_markup=menu_builder.as_markup()
    )
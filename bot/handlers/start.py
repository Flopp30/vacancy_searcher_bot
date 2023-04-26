"""
start handler
"""
from aiogram import types

from bot.text_for_messages import TEXT_GREETING
from bot.structure.keyboards import main_menu


async def start(message: types.Message) -> None:

    await message.answer(
        TEXT_GREETING,
        reply_markup=main_menu()
    )

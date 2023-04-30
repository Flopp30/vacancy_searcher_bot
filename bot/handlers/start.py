"""
start handler
"""
from aiogram import types

from bot.structure.keyboards import MENU_BOARD
from bot.text_for_messages import TEXT_GREETING


async def start(message: types.Message) -> None:

    await message.answer(
        TEXT_GREETING,
        reply_markup=MENU_BOARD
    )

"""
start handler
"""
from aiogram import types

from bot.text_for_messages import TEXT_GREETING


async def start(message: types.Message) -> None:

    await message.answer(
        TEXT_GREETING,
    )

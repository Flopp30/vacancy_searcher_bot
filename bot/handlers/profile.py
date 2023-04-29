from aiogram import types
from aiogram.enums import ParseMode

from bot.text_for_messages import TEXT_PROFILE


async def profile(message: types.Message) -> None:

    await message.answer(
        TEXT_PROFILE,
        parse_mode=ParseMode.HTML
    )

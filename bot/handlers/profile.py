from aiogram import types
from aiogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

from bot.db import get_profile_by_user_id
from bot.structure.keyboards import PROFILE_BOARD
from bot.text_for_messages import TEXT_PROFILE
from bot.utils import profile_main_message_formatter


async def profile_info(message: types.Message, session_maker: sessionmaker) -> types.Message:
    """
    Profile handler. Main
    """
    user_profile = await get_profile_by_user_id(user_id=message.from_user.id, session=session_maker)
    if not user_profile:
        return await message.answer("Здесь пока ничего нет :(")
    message_args = await profile_main_message_formatter(user_profile)

    text = TEXT_PROFILE.format(**message_args)
    return await message.answer(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=PROFILE_BOARD
    )

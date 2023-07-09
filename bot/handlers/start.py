"""
start handler
"""
from aiogram import types

from bot.structure.keyboards import get_main_menu_board
from bot.text_for_messages import TEXT_GREETING
from db import profile_crud


async def start(message: types.Message, get_async_session) -> None:
    async with get_async_session() as session:
        is_new = not bool(
            await profile_crud.get_by_attribute(
                attr_name="user_id",
                attr_value=message.from_user.id,
                session=session,
                is_deleted=False
            )
        )
    await message.answer(
        TEXT_GREETING,
        reply_markup=get_main_menu_board(user_id=message.from_user.id, is_new=is_new)
    )

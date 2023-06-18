from aiogram import types
from aiogram.enums import ParseMode

from bot.structure.keyboards import PROFILE_BOARD
from bot.text_for_messages import TEXT_PROFILE
from bot.utils import profile_main_message_formatter

from db.crud.profile import profile_crud


async def profile_info(message: types.Message, get_async_session) -> types.Message:
    """
    Profile handler. Main
    """
    async with get_async_session() as session:
        user_profile = await profile_crud.get_profile_by_attribute(
            attr_name='user_id',
            attr_value=message.from_user.id,
            session=session,
            is_deleted=False
        )

    if not user_profile:
        return await message.answer("Сначала профиль, потом вакансии :)")
    message_args = await profile_main_message_formatter(user_profile)

    text = TEXT_PROFILE.format(**message_args)
    return await message.answer(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=PROFILE_BOARD
    )

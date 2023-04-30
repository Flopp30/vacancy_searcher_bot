from aiogram import types
from aiogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

from bot.db import get_profile_by_user_id, Profile
from bot.structure.keyboards import MENU_BOARD
from bot.text_for_messages import TEXT_PROFILE


async def profile(message: types.Message, session_maker: sessionmaker) -> None:
    message_args = {}
    user_profile = await get_profile_by_user_id(user_id=message.from_user.id, session=session_maker)
    user_profile: Profile
    message_args['professional_role'] = user_profile.professional_role \
        if user_profile.professional_role else 'Не заполнено'
    message_args['region'] = user_profile.region if user_profile.region else 'Не заполнено'
    message_args['ready_for_relocation'] = 'Да' if user_profile.ready_for_relocation else 'Нет'
    message_args['salary_from'] = user_profile.salary_from if user_profile.salary_from else 'Не заполнено'
    message_args['salary_to'] = user_profile.salary_to if user_profile.salary_to else ''
    message_args['work_type'] = user_profile.work_type if user_profile.work_type else ''
    text = TEXT_PROFILE.format(**message_args)
    await message.answer(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=MENU_BOARD
    )

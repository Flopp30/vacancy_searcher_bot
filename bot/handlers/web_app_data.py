import asyncio
import json

from aiogram import types
from sqlalchemy.orm import sessionmaker

from bot.handlers import profile_info, start
from bot.settings import logger
from db import get_profile_by_user_id, create_profile
from db.crud.profile import update_profile


async def web_app_data_receive(message: types.Message, session_maker: sessionmaker):
    await asyncio.sleep(0.1)
    data = json.loads(message.web_app_data.data)
    profile_args = {}
    logger.debug(f"From web app returned data: {data}")
    for field_name, field_value in data.items():
        if field_value is not None:
            profile_args[field_name] = field_value
    profile = await get_profile_by_user_id(user_id=message.from_user.id, session=session_maker)
    if not profile:
        profile = await create_profile(user_id=message.from_user.id, session=session_maker)
    logger.debug(f"Profile {profile.id} updating with data {profile_args}")
    try:
        await update_profile(profile, profile_args, session_maker)
        logger.debug(f"Profile {profile.id} updated successful")
        await message.answer("Данные успешно обновлены")
        return await profile_info(message, session_maker)
    except Exception as e:
        await message.answer("Произошла ошибка при обновлении профиля. Попробуйте ещё раз")
        logger.error(f"An error occurred while updating the profile."
                     f"Profile: {profile.id}"
                     f"Exc: {e}")
        return await start(message)

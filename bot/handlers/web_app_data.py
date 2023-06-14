import asyncio

from aiogram import types
import json

from sqlalchemy.orm import sessionmaker

from db import update_object, Profile, get_profile_by_user_id, GradeTypes, WorkTypes, create_profile
from bot.handlers import profile_info, start
from bot.settings import logger


async def web_app_data_receive(message: types.Message, session_maker: sessionmaker):
    await asyncio.sleep(0.1)
    data = json.loads(message.web_app_data.data)
    profile_args = {}
    logger.debug(f"From web app returned data: {data}")
    for field_name, field_value in data.items():
        match field_name:
            case "work_type":
                field_value = WorkTypes(field_value).value
            case "grade":
                field_value = GradeTypes(field_value).value
        if field_value is not None:
            profile_args[field_name] = field_value
    profile = await get_profile_by_user_id(user_id=message.from_user.id, session=session_maker)
    if not profile:
        profile = await create_profile(user_id=message.from_user.id, session=session_maker)
    logger.debug(f"Profile {profile.id} updating with data {profile_args}")
    try:
        await update_object(Profile, profile.id, profile_args, session_maker)
        logger.debug(f"Profile {profile.id} updated successful")
        await message.answer("Данные успешно обновлены")
        return await profile_info(message, session_maker)
    except Exception as e:
        await message.answer("Произошла проблема при обновлении профиля. Попробуйте ещё раз")
        logger.error(f"An error occurred while updating the profile."
                     f"Profile: {profile.id}"
                     f"Exc: {e}")
        return await start(message)

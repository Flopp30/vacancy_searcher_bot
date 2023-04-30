import asyncio

from aiogram import types
import json

from sqlalchemy.orm import sessionmaker

from bot.db import update_object, Profile, get_profile_by_user_id
from bot.db.profile import GradeTypes, WorkTypes


async def web_app_data_receive(message: types.Message, session_maker: sessionmaker):
    await asyncio.sleep(0.1)
    data = json.loads(message.web_app_data.data)
    profile_args = {}
    for field_name, field_value in data.items():
        match field_name:
            case 'work_type':
                field_value = WorkTypes(field_value).value
            case 'grade':
                field_value = GradeTypes(field_value).value
        profile_args[field_name] = field_value
    profile = await get_profile_by_user_id(user_id=message.from_user.id, session=session_maker)
    await update_object(Profile, profile.id, profile_args, session_maker)
    await message.answer("Данные успешно обновлены")

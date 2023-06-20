import asyncio
import json

from aiogram import types

from bot.handlers import profile_info, start
from bot.settings import bot_logger as logger
from db.crud.profile import profile_crud
from db.crud.base import grade_types_crud, work_types_crud


async def web_app_data_receive(message: types.Message, get_async_session):
    await asyncio.sleep(0.1)
    data = json.loads(message.web_app_data.data)
    profile_args = {}
    logger.debug(f"From web app returned data: {data}")
    for field_name, field_value in data.items():
        if field_value is not None:
            if field_name in ('salary_from', 'salary_to'):
                profile_args[field_name] = int(field_value)
            elif field_name == 'grade':
                async with get_async_session() as session:
                    grade = await grade_types_crud.get_by_attribute('type', field_value, session=session)
                profile_args['grade_type_id'] = grade.id
            elif field_name == 'work_type':
                async with get_async_session() as session:
                    work_type = await work_types_crud.get_by_attribute('type', field_value, session=session)
                profile_args['work_type_id'] = work_type.id
            else:
                profile_args[field_name] = field_value

    async with get_async_session() as session:
        profile = await profile_crud.get_profile_by_attribute(
            attr_name='user_id',
            attr_value=message.from_user.id,
            session=session,
            is_deleted=False
        )

    if not profile:
        profile_args['user_id'] = message.from_user.id
        async with get_async_session() as session:
            profile = await profile_crud.create(profile_args, session=session)
    logger.debug(f"Profile {profile.id} updating with data {profile_args}")

    try:
        async with get_async_session() as session:
            profile = await profile_crud.update(profile, profile_args, session=session)
        logger.debug(f"Profile {profile.id} updated successful")
        await message.answer("Данные успешно обновлены")
        return await profile_info(message, get_async_session=get_async_session)
    except Exception as e:
        await message.answer("Произошла ошибка при обновлении профиля. Попробуйте ещё раз")
        logger.error(f"An error occurred while updating the profile."
                     f"Profile: {profile.id}"
                     f"Exc: {e}")
        return await start(message)

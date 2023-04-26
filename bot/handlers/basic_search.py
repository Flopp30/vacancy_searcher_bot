"""
Basic search
"""
import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.db import is_user_exist, get_user, get_humanize_exp, get_hh_exp
from bot.structure.callback_data_states import SearchCallBack
from bot.structure.keyboards import paginator_keyboard
from bot.text_for_messages import TEXT_CURRENT_MESSAGE_PAGINATOR
from bot.utils import get_data_from_hh, make_messages


async def vacancy_basic_search_main(
        message: types.Message,
        session_maker: sessionmaker,
        state: FSMContext
):
    """
    basic search main
    :param message:
    :param session_maker:
    :param state:
    :return:
    """
    if not await is_user_exist(message.from_user.id, session=session_maker):
        return await message.answer('Сначала нужно создать профиль для поиска вакансий /profile')
    user = await get_user(message.from_user.id, session=session_maker)
    human_grade = get_humanize_exp(user.grade)
    hh_grade = get_hh_exp(user.grade)
    await message.answer(
        f'Вот вакансии под твой профиль\n'
        f'Специальность: {user.professional_role}\n'
        f'Опыт работы:{human_grade}')
    vacancies = await asyncio.create_task(get_data_from_hh(vacancy_name=user.professional_role, grade=hh_grade))
    messages = await asyncio.create_task(make_messages(vacancies))
    if messages:
        text = messages[0] + TEXT_CURRENT_MESSAGE_PAGINATOR.format(
            current_message=1,
            len_messages=len(messages)
        )
        await message.answer(
            text=text,
            reply_markup=paginator_keyboard()
        )
    else:
        await message.answer(
            text="Поиск не дал результата :("
        )

    await state.update_data(messages=messages, current_message=0)


async def switch_message_page_callback(
        callback_query: types.CallbackQuery,
        callback_data: SearchCallBack,
        state: FSMContext
):
    """
    message paginator
    :param callback_query:
    :param callback_data:
    :param state:
    :return:
    """
    data = await state.get_data()
    messages = data.get("messages")
    current_message = data.get("current_message")

    if callback_data.direction == "prev":
        if current_message == 0:
            return
        current_message -= 1
    elif callback_data.direction == "next":
        if current_message == len(messages) - 1:
            return
        current_message += 1

    await state.update_data(current_message=current_message)
    text = messages[current_message] + TEXT_CURRENT_MESSAGE_PAGINATOR.format(
        current_message=current_message + 1,
        len_messages=len(messages)
    )
    await callback_query.message.edit_text(
        text=text,
        reply_markup=callback_query.message.reply_markup
    )

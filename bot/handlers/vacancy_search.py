"""
Vacancy search by profile
"""
from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.settings import VACANCY_TO_SHOW_COUNT
from bot.structure import SearchCallBack
from bot.structure.keyboards import PAGINATOR_BOARD
from bot.text_for_messages import TEXT_CURRENT_MESSAGE_PAGINATOR
from bot.utils import make_get_params_from_profile, get_data_from_hh, make_messages

from db import get_profile_by_user_id


async def vacancy_search_by_callback(
        callback_query: types.CallbackQuery,
        session_maker: sessionmaker,
        state: FSMContext
):
    user_profile = await get_profile_by_user_id(user_id=callback_query.from_user.id, session=session_maker)
    get_params = await make_get_params_from_profile(user_profile)
    vacancies = await get_data_from_hh(get_params=get_params, vacancy_count=VACANCY_TO_SHOW_COUNT)
    if vacancies:
        messages = await make_messages(vacancies)
        text = messages[0] + TEXT_CURRENT_MESSAGE_PAGINATOR.format(
            current_message=1,
            len_messages=len(messages)
        )
        await state.update_data(messages=messages, current_message=0)

        return await callback_query.message.edit_text(
            text=text,
            reply_markup=PAGINATOR_BOARD
        )
    else:
        return await callback_query.message.edit_text(
            text="Поиск не дал результата. Попробуйте изменить данные в профиле",
        )


async def vacancy_search(
        message: types.Message,
        session_maker: sessionmaker,
        state: FSMContext
) -> types.Message:
    """
    search handler. Main
    """
    user_profile = await get_profile_by_user_id(user_id=message.from_user.id, session=session_maker)
    if not user_profile:
        return await message.answer("Для поиска вакансий тебе необходимо создать профиль")
    get_params = await make_get_params_from_profile(user_profile)
    vacancies = await get_data_from_hh(get_params=get_params, vacancy_count=VACANCY_TO_SHOW_COUNT)
    if vacancies:
        messages = await make_messages(vacancies)
        text = messages[0] + TEXT_CURRENT_MESSAGE_PAGINATOR.format(
            current_message=1,
            len_messages=len(messages)
        )
        await state.update_data(messages=messages, current_message=0)

        return await message.answer(
            text=text,
            reply_markup=PAGINATOR_BOARD
        )
    else:
        return await message.answer(
            text="Поиск не дал результата :("
        )


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

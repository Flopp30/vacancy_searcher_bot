"""
Advanced search
"""
import asyncio
import logging

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.db import get_hh_exp
from bot.structure import AdvSearchStates, ExpTypeCallBack
from bot.structure.keyboards import paginator_keyboard, exp_type_keyboard
from bot.text_for_messages import TEXT_CURRENT_MESSAGE_PAGINATOR
from bot.utils import get_data_from_hh, make_messages
from bot.utils.validators import vacancy_count_validator


async def adv_search_main(
        message: types.Message,
        state: FSMContext
):
    """
    Adv search main
    :param message:
    :param state:
    :return:
    """

    await state.set_state(AdvSearchStates.waiting_for_prof_role)
    await message.answer('Пришлите ключевое слово для поиска (н-р: Java developer)')


async def adv_search_prof_role(
        message: types.Message,
        state: FSMContext,
):
    """
    Prof type handler
    :param message:
    :param state:
    :return:
    """
    await state.update_data(prof_role=message.text)
    await state.set_state(AdvSearchStates.waiting_for_exp)
    await message.answer('Отлично, теперь выберем ваш опыт работы', reply_markup=exp_type_keyboard())


async def adv_search_exp_type(
        callback_query: types.CallbackQuery,
        callback_data: ExpTypeCallBack,
        state: FSMContext,
):
    """
    exp type handler
    :param callback_query:
    :param callback_data:
    :param state:
    :return:
    """
    hh_exp = get_hh_exp(callback_data.grade)
    await state.update_data(grade=hh_exp)
    await state.set_state(AdvSearchStates.waiting_for_number_of_vacancies)
    await callback_query.message.answer('Гуд! Теперь давай определимся с тем, сколько вакансий тебе нужно.\n'
                                        'Только давай честно, я больше 30 тебе не покажу :)\n'
                                        'В ответ отправь просто число')


async def adv_search_show_vacancies(
        message: types.Message,
        state: FSMContext,
):
    """
    result adv search
    :param message:
    :param state:
    :return:
    """
    number_of_vacancies = message.text
    if not vacancy_count_validator(message.text):
        await message.answer('Ведь просил же. Все равно будет 30 :)')
        number_of_vacancies = 30
    data = await state.get_data()
    search_args = {
        'number_of_vacancies': int(number_of_vacancies),
        'vacancy_name': data.get('prof_role'),
        'grade': data.get('grade'),
    }
    await state.clear()
    logging.info('Отправлены запросы к hh')
    vacancies = await asyncio.create_task(get_data_from_hh(**search_args))
    logging.info('Получены овтеты от hh')
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

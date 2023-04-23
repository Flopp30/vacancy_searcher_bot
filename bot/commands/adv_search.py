import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.commands.search import paginator_markup_builder
from bot.utils import get_data_from_hh, make_messages


async def vacancy_advanced_search(message: types.Message, state: FSMContext):
    vacancies = await asyncio.create_task(get_data_from_hh(message.text))
    messages = await asyncio.create_task(make_messages(vacancies))
    if messages:
        await message.answer(
            messages[0],
            reply_markup=paginator_markup_builder.as_markup()
        )
    else:
        await message.answer(
            text="Поиск не дал результата :("
        )

    await state.update_data(messages=messages, current_message=0)

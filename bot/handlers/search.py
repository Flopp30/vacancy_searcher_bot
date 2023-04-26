import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.structure.callback_data_states import SearchCallBack
from bot.structure.keyboards import paginator_keyboard
from bot.utils import get_data_from_hh, make_messages


async def vacancy_basic_search(message: types.Message, state: FSMContext):
    vacancies = await asyncio.create_task(get_data_from_hh(message.text))
    messages = await asyncio.create_task(make_messages(vacancies))
    if messages:
        await message.answer(
            messages[0],
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

    await callback_query.message.edit_text(
        text=messages[current_message],
        reply_markup=callback_query.message.reply_markup
    )

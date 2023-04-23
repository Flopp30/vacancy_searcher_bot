import asyncio

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.commands.callback_data_states import SearchCallBack
from bot.utils import get_data_from_hh, make_messages

paginator_markup_builder = InlineKeyboardBuilder()

paginator_markup_builder.button(
    text="<<", callback_data=SearchCallBack(direction="prev")
)
paginator_markup_builder.button(
    text=">>", callback_data=SearchCallBack(direction="next")
)


async def vacancy_basic_search(message: types.Message, state: FSMContext):
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

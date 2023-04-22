import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from bot_markup import paginator_markup
from config import (
    TG_BOT_KEY,
    logging,
    TEXT_GREETING,
    TEXT_VACANCY_SEARCH,
    TEXT_SEARCH_WITHOUT_COMMAND,
    TEXT_HELP
)
from utils import get_data_from_hh, make_messages

bot = Bot(token=TG_BOT_KEY, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class ChatState(StatesGroup):
    waiting_for_chat_command = State()


@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.answer(TEXT_HELP)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(TEXT_GREETING)


@dp.message_handler(commands=['search'])
async def chat(message: types.Message):
    await message.answer(TEXT_VACANCY_SEARCH)
    await ChatState.waiting_for_chat_command.set()


@dp.message_handler()
async def chat(message: types.Message):
    await message.answer(TEXT_SEARCH_WITHOUT_COMMAND)


@dp.message_handler(state=ChatState.waiting_for_chat_command)
async def vacancy_searcher(message: types.Message, state: FSMContext):
    await state.reset_state()

    vacancies = await asyncio.create_task(get_data_from_hh(message.text))
    messages = await asyncio.create_task(make_messages(vacancies))

    await message.answer(messages[0], reply_markup=paginator_markup)

    await state.update_data(messages=messages, current_message=0)


@dp.callback_query_handler(lambda c: c.data in ["prev", "next"])
async def switch_message_page(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    messages = data.get("messages")
    current_message = data.get("current_message")

    if callback_query.data == "prev":
        if current_message == 0:
            return
        current_message -= 1
    elif callback_query.data == "next":
        if current_message == len(messages) - 1:
            return
        current_message += 1

    await state.update_data(current_message=current_message)

    await bot.edit_message_text(
        text=messages[current_message],
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        reply_markup=paginator_markup,
        )


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logging.error(e)
    finally:
        logging.info('Bot stopped')

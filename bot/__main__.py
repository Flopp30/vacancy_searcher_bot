"""
Main
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers import register_user_commands, BOT_COMMANDS_INFO
from bot.db import (
    create_async_engine,
    proceed_schemas,
    get_session_maker,
    BaseModel,
)
from bot.settings import TG_BOT_KEY, POSTGRES_URL


async def async_main() -> None:

    # init dispatcher and bot
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    bot = Bot(token=TG_BOT_KEY)
    # handlers
    commands_for_bot = []
    for cmd in BOT_COMMANDS_INFO:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands_for_bot)
    register_user_commands(dp)
    # db
    async_engine = create_async_engine(POSTGRES_URL)
    session_maker = await get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)
    # start
    await dp.start_polling(bot, session_maker=session_maker)


def main():
    try:
        asyncio.run(async_main())
    except (KeyboardInterrupt, SystemExit):
        logging.debug("Bot stopped")


if __name__ == "__main__":
    main()

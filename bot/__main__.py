"""
Main
"""
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from db import bot_get_async_session
from bot.handlers import register_user_commands, BOT_COMMANDS_INFO
from bot.settings import (
    TG_BOT_KEY,
    bot_logger as logger
)


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

    await dp.start_polling(bot, get_async_session=bot_get_async_session)


def main():
    try:
        asyncio.run(async_main())
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Bot stopped")


if __name__ == "__main__":
    main()

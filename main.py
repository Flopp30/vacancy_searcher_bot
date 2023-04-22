from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import TG_BOT_KEY, logging


bot = Bot(token=TG_BOT_KEY, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет! Я Job.')


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=False)
    except Exception as e:
        logging.error(e)
    finally:
        logging.info('Bot stopped')

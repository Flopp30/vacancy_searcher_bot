"""
Config file
"""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv


# logging
bot_logger = logging.getLogger('telegram_bot')
bot_logger.setLevel(logging.DEBUG)

bot_file_handler = logging.FileHandler('../bot.log')
bot_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot_file_handler.setFormatter(bot_formatter)
bot_logger.addHandler(bot_file_handler)


# Dirs
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# Bot
WEB_APP_URL = os.getenv("WEB_APP_URL")

# Keys
TG_BOT_KEY = os.getenv("TG_BOT_KEY")

EMAIL_REG_EXP = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

NAME_REG_EXP = r"^[A-Za-zА-ЯЁа-яё]+$"

# Request
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}
VACANCY_TO_SHOW_COUNT = 10

# Parsing
PARS_KEYS = {
    "vacancy_name": ["name"],
    "area_name": ["area", "name"],
    "salary_from": ["salary", "from"],
    "salary_to": ["salary", "to"],
    "salary_currency": ["salary", "currency"],
    "address_raw": ["address", "raw"],
    "experience": ["experience", "name"],
    "employment": ["employment", "name"],
    "url": ["alternate_url"],
    "published": ["published_at"],
}

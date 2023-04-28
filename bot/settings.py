"""
Config file
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

# Dirs
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# Keys
TG_BOT_KEY = os.getenv("TG_BOT_KEY")

# DB
DB_DRIVER = os.getenv("DB_DRIVER", "postgresql+asyncpg")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "ja_bot")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

POSTGRES_URL = URL.create(
    drivername=DB_DRIVER,
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)

EMAIL_REG_EXP = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"

NAME_REG_EXP = r"^[A-Za-zА-ЯЁа-яё]+$"

NUMBER_IS_LESS_31_REG_EXP = "^([1-2]?[0-9]|30)$"

# Request
URL = "https://api.hh.ru/vacancies/"
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

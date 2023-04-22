import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Dirs
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

# Keys
TG_BOT_KEY = os.getenv("TG_BOT_KEY")

# Logging
logging.basicConfig(level=logging.INFO)

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

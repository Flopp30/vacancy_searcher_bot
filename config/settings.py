import os
import logging
from pathlib import Path

from dotenv import load_dotenv

# Dirs
BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / '.env')

# Keys
TG_BOT_KEY = os.getenv('TG_BOT_KEY')

# Logging
logging.basicConfig(level=logging.INFO)

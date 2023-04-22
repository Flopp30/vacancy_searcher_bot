from config.settings import (
    logging,
    TG_BOT_KEY,
    URL,
    HEADERS,
    VACANCY_TO_SHOW_COUNT,
    PARS_KEYS
)
from config.texts import (
    TEXT_GREETING,
    TEXT_VACANCY_SEARCH,
    TEXT_SEARCH_WITHOUT_COMMAND,
    TEXT_HELP,
    TEXT_PROFILE_GET_NAME,
    TEXT_PROFILE_GET_PROF_ROLE,
    TEXT_PROFILE_GET_EXPERIENCE,
)

__all__ = [
    # settings
    TG_BOT_KEY,
    logging,
    URL,
    HEADERS,
    VACANCY_TO_SHOW_COUNT,
    PARS_KEYS,

    # texts
    TEXT_GREETING,
    TEXT_VACANCY_SEARCH,
    TEXT_SEARCH_WITHOUT_COMMAND,
    TEXT_HELP,
    TEXT_PROFILE_GET_NAME,
    TEXT_PROFILE_GET_PROF_ROLE,
    TEXT_PROFILE_GET_EXPERIENCE,
]

"""
Register handlers
"""
from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command

from bot.handlers.help import help_command, help_func
from bot.handlers.profile import profile_info
from bot.handlers.start import start
from bot.handlers.vacancy_search import vacancy_search, switch_message_page_callback, vacancy_search_by_callback
from bot.handlers.web_app_data import web_app_data_receive
from bot.middleware import RegisterCheck
from bot.structure import SearchCallBack, ProfileCallback
from bot.text_for_messages import BOT_COMMANDS_INFO

__all__ = [
    "BOT_COMMANDS_INFO",
    "register_user_commands",
]


def register_user_commands(router: Router) -> None:
    """
    Register user commands
    :param router:
    :return:
    """

    # middleware
    router.message.middleware(RegisterCheck())
    router.callback_query.middleware(RegisterCheck())
    # start
    router.message.register(start, CommandStart())

    # help
    router.message.register(help_command, Command(commands=["help"]))
    router.message.register(help_func, F.text.capitalize() == "Помощь")

    # profile
    router.message.register(profile_info, Command(commands=["profile"]))
    router.message.register(profile_info, F.text.capitalize() == "Посмотреть профиль")
    router.callback_query.register(vacancy_search_by_callback, ProfileCallback.filter())

    # vacancy search
    router.message.register(vacancy_search, Command(commands=["search"]))
    router.message.register(vacancy_search, F.text.capitalize() == "Поиск вакансий")
    router.callback_query.register(switch_message_page_callback, SearchCallBack.filter())

    # web app
    router.message.register(web_app_data_receive, F.content_type.in_(ContentType.WEB_APP_DATA, ))

"""
Register handlers
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command

from bot.handlers.help import help_command, help_func
from bot.handlers.profile import profile_info
from bot.handlers.start import start
from bot.handlers.vacancy_search import switch_message_page_callback, vacancy_search_by_callback
from bot.middleware import RegisterCheck
from bot.structure import SearchCallBack, ProfileCallback, MainMenuCallBack, MainMenuCDAction, ProfileCDAction
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
    router.callback_query.register(
        profile_info, MainMenuCallBack.filter(
            F.action == MainMenuCDAction.SHOW_PROFILE
        )
    )
    router.callback_query.register(
        vacancy_search_by_callback,
        MainMenuCallBack.filter(
            F.action == MainMenuCDAction.SHOW_VACANCIES
        )
    )

    # help
    router.message.register(help_command, Command(commands=["help"]))
    router.message.register(help_func, F.text.capitalize() == "Помощь")
    # profile
    router.callback_query.register(
        vacancy_search_by_callback,
        ProfileCallback.filter(
            F.action == ProfileCDAction.SHOW_VACANCIES
        )
    )

    # vacancy search
    router.callback_query.register(switch_message_page_callback, SearchCallBack.filter())

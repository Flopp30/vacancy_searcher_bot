from aiogram.filters import CommandStart, Command

from bot.bot_messages import BOT_COMMANDS_INFO
from bot.commands.adv_search import vacancy_advanced_search
from bot.commands.callback_data_states import SearchCallBack
from bot.commands.profile import profile
from bot.commands.start import start
from bot.commands.help import help_command, help_func
from bot.commands.search import vacancy_basic_search, switch_message_page_callback
from aiogram import Router, F

__all__ = [
    "BOT_COMMANDS_INFO",
    "register_user_commands",
]


def register_user_commands(router: Router) -> None:
    router.message.register(start, CommandStart())

    # help
    router.message.register(help_command, Command(commands=["help"]))
    router.message.register(help_func, F.text == "Помощь")

    # profile
    router.message.register(profile, Command(commands=["profile"]))
    router.message.register(profile, F.text == "Профиль")

    # search
    router.message.register(vacancy_basic_search, Command(commands=["search"]))
    router.message.register(vacancy_basic_search, F.text == "Поиск по вакансиям")
    router.callback_query.register(switch_message_page_callback, SearchCallBack.filter())

    # adv search
    router.message.register(vacancy_advanced_search, Command(commands=["adv_search"]))
    router.message.register(vacancy_advanced_search, F.text == "Расширенный поиск")
    router.callback_query.register(switch_message_page_callback, SearchCallBack.filter())

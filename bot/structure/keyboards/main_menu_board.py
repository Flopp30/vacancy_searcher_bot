from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.settings import WEB_APP_URL
from bot.structure.callback_data_states import MainMenuCallBack, MainMenuCDAction


def get_main_menu_board(user_id: int, is_new: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_new:
        builder.button(
            text="Создать профиль", web_app=WebAppInfo(url=WEB_APP_URL + f"/profile/{user_id}")
        )
    else:
        builder.button(
            text="Редактировать профиль", web_app=WebAppInfo(url=WEB_APP_URL + f"/profile/{user_id}")
        )
        builder.button(
            text="Посмотреть профиль", callback_data=MainMenuCallBack(action=MainMenuCDAction.SHOW_PROFILE)
        )
        builder.button(
            text="Показать вакансии", callback_data=MainMenuCallBack(action=MainMenuCDAction.SHOW_VACANCIES)
        )

    builder.adjust(1)

    return builder.as_markup()

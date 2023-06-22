"""
Callback datas
"""
import enum

from aiogram.filters.callback_data import CallbackData


class SearchCallBack(CallbackData, prefix="pagination"):
    """
    paginator callback. return pagination direction
    """
    direction: str  # "prev" | "next"


class ProfileCDAction(enum.IntEnum):
    SHOW_VACANCIES = 0


class ProfileCallback(CallbackData, prefix="profile"):
    """
    Next step after profile
    """
    action: ProfileCDAction


class MainMenuCDAction(enum.IntEnum):
    """
        Действия с постами
    """
    SHOW_PROFILE = 0
    SHOW_VACANCIES = 1


class MainMenuCallBack(CallbackData, prefix="main_menu"):
    """
    Main menu callback
    """
    action: MainMenuCDAction

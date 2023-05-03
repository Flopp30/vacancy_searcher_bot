"""
Callback datas
"""
from aiogram.filters.callback_data import CallbackData


class SearchCallBack(CallbackData, prefix="pagination"):
    """
    paginator callback. return pagination direction
    """
    direction: str  # "prev" | "next"


class ProfileCallback(CallbackData, prefix="profile"):
    """
    Next step after profile
    """
    action: str  # "search" | ..

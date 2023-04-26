"""
Callback datas
"""
from aiogram.filters.callback_data import CallbackData


class SearchCallBack(CallbackData, prefix="pagination"):
    """
    paginator callback. return pagination direction
    """
    direction: str  # "prev" | "next"


class ProfileCallBack(CallbackData, prefix="profile"):
    """
    profile callback. return editing type (web app / in bot)
    """
    type: str  # "web" | "inline"


class FieldTypeToUpdateCallBack(CallbackData, prefix="partial_update"):
    """
    field type to update. return firstname, lastname etc..
    """
    field: str  # "firstname" | "lastname" | ...


class ExpTypeCallBack(CallbackData, prefix="experience"):
    """
    return grade on inline buttons with exp text (jun, middle, senior)
    """
    grade: str  # "jun" | "middle" | "senior"


class NextStepCallBack(CallbackData, prefix=""):
    """
    next step after profile partial editing. return main / editing.
    """
    step: str  # "main" | "editing"

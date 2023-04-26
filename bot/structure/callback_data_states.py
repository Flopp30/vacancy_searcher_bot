from aiogram.filters.callback_data import CallbackData


class SearchCallBack(CallbackData, prefix="pagination"):
    direction: str  # "prev" | "next"


class ProfileCallBack(CallbackData, prefix="profile"):
    type: str  # "web" | "inline"


class FieldTypeToUpdateCallBack(CallbackData, prefix="partial_update"):
    field: str  # "firstname" | "lastname" | ...


class ExpTypeCallBack(CallbackData, prefix="experience"):
    grade: str  # "jun" | "middle" | "senior"


class NextStepCallBack(CallbackData, prefix=""):
    step: str  # "main" | "editing"

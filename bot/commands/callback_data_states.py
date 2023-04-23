from aiogram.filters.callback_data import CallbackData


class SearchCallBack(CallbackData, prefix="pagination"):
    direction: str  # "prev" | "next"
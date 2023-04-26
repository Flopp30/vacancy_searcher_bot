from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.structure.callback_data_states import SearchCallBack


def paginator_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="<<", callback_data=SearchCallBack(direction="prev")
    )
    builder.button(
        text=">>", callback_data=SearchCallBack(direction="next")
    )

    return builder.as_markup()

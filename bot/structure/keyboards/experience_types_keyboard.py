from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db import GradeTypes
from bot.structure.callback_data_states import ExpTypeCallBack


def exp_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Нет опыта", callback_data=ExpTypeCallBack(grade=GradeTypes.JUNIOR.value)
    )
    builder.button(
        text="1-3 года", callback_data=ExpTypeCallBack(grade=GradeTypes.MIDDLE.value)
    )
    builder.button(
        text="Больше 3 лет", callback_data=ExpTypeCallBack(grade=GradeTypes.SENIOR.value)
    )

    builder.button(
        text="Отмена", callback_data=ExpTypeCallBack(grade='cancel')
    )
    builder.adjust(1)
    return builder.as_markup()

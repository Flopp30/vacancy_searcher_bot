"""
Cancel keyboard
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    cancel keyboard builder
    :return:
    """
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Отмена'))
    return builder.as_markup(resize_keyboard=True)

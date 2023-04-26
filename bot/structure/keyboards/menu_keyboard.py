"""
Main keyboard
"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu() -> ReplyKeyboardMarkup:
    """
    main menu keyboard builder
    :return:
    """
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Поиск по вакансиям"),
        KeyboardButton(text="Расширенный поиск"),
    )
    builder.row(
        KeyboardButton(text="Профиль"),
        KeyboardButton(text="Помощь"),
    )
    return builder.as_markup(resize_keyboard=True)

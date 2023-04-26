"""
profile menus builders
"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db import UserFieldsToUpdate
from bot.structure import (
    ProfileCallBack,
    FieldTypeToUpdateCallBack,
    NextStepCallBack
)


def profile_inline_menu() -> InlineKeyboardMarkup:
    """
    Profile inline menu builder
    :return:
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Web-формой", callback_data=ProfileCallBack(type="web")
    )
    builder.button(
        text="Прямо в чате", callback_data=ProfileCallBack(type="inline")
    )
    builder.adjust(1)
    return builder.as_markup()


def profile_choose_field_to_update_keyboard() -> InlineKeyboardMarkup:
    """
    profile fields inline keyboard builder
    :return:
    """
    builder = InlineKeyboardBuilder()
    for field in UserFieldsToUpdate.choices():
        builder.button(
            text=field[1], callback_data=FieldTypeToUpdateCallBack(field=field[0])
        )
    builder.button(
        text='Отмена', callback_data=FieldTypeToUpdateCallBack(field='cancel')
    )
    builder.adjust(1)
    return builder.as_markup()


def profile_next_step_keyboard() -> InlineKeyboardMarkup:
    """
    next step inline menu builder
    :return:
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="На главную", callback_data=NextStepCallBack(step="main")
    )
    builder.button(
        text="Редактировать профиль", callback_data=NextStepCallBack(step="editing")
    )

    builder.adjust(1)
    return builder.as_markup()

"""
Profile editing
"""
from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.db import get_user, update_user, get_humanize_exp
from bot.handlers.profile_create import profile_main
from bot.handlers.start import start
from bot.structure import (
    ProfileUpdateStates,
    FieldTypeToUpdateCallBack,
    NextStepCallBack,
    ExpTypeCallBack
)
from bot.structure.keyboards import (
    profile_choose_field_to_update_keyboard,
    exp_type_keyboard,
    cancel_keyboard,
    profile_next_step_keyboard,
)
from bot.text_for_messages import (
    TEXT_PROFILE_PARTIAL_UPDATE,
    TEXT_PROFILE_FIRSTNAME,
    TEXT_PROFILE_LASTNAME,
    TEXT_PROFILE_EMAIL,
    TEXT_PROFILE_PROF_ROLE,
    TEXT_PROFILE_EXP,
    TEXT_PROFILE_CANCEL,
    TEXT_PROFILE_PARTIAL_UPDATE_SUCCESS,
    TEXT_INVALID_FIST_LASTNAME,
    TEXT_INVALID_EMAIL
)
from bot.utils.validators import user_field_validator


async def profile_edit(callback_query: types.CallbackQuery, session_maker: sessionmaker, state: FSMContext):
    """
    Partial editing user's profile
    :param callback_query:
    :param session_maker:
    :param state:
    :return:
    """
    user = await get_user(callback_query.from_user.id, session=session_maker)
    await state.set_state(ProfileUpdateStates.waiting_for_choose_field)
    grade = get_humanize_exp(user.grade)
    text = TEXT_PROFILE_PARTIAL_UPDATE.format(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        prof_role=user.professional_role,
        exp=grade
    )
    await callback_query.message.answer(
        text=text,
        reply_markup=profile_choose_field_to_update_keyboard()
    )


async def profile_edit_choose_field(
        callback_query: types.CallbackQuery,
        callback_data: FieldTypeToUpdateCallBack,
        state: FSMContext,
):
    """
    Callback handler, return message with text about choose field
    :param callback_query:
    :param callback_data:
    :param state:
    :return:
    """
    await state.set_state(ProfileUpdateStates.waiting_for_partial_update_data)
    await state.update_data(field=callback_data.field)
    cancel_board = cancel_keyboard()

    match callback_data.field:
        case "firstname":
            await callback_query.message.answer(
                text=TEXT_PROFILE_FIRSTNAME,
                reply_markup=cancel_board
            )

        case "lastname":
            await callback_query.message.answer(
                text=TEXT_PROFILE_LASTNAME,
                reply_markup=cancel_board
            )

        case "email":
            await callback_query.message.answer(
                text=TEXT_PROFILE_EMAIL,
                reply_markup=cancel_board
            )

        case "professional_role":
            await callback_query.message.answer(
                text=TEXT_PROFILE_PROF_ROLE,
                reply_markup=cancel_board
            )

        case "grade":
            await callback_query.message.answer(
                text=TEXT_PROFILE_EXP,
                reply_markup=exp_type_keyboard()
            )

        case "cancel":
            return await start(callback_query.message)


async def profile_partial_update_grade(
        callback_query: types.CallbackQuery,
        callback_data: ExpTypeCallBack,
        session_maker: sessionmaker,
        state: FSMContext,
):
    """
    Callback handler to update profile grade
    :param callback_query:
    :param callback_data:
    :param session_maker:
    :param state:
    :return:
    """
    if callback_data.grade == "cancel":
        await callback_query.message.answer(TEXT_PROFILE_CANCEL)
        return await start(callback_query.message)
    await update_user(
        user_id=callback_query.from_user.id,
        fields={
            "grade": callback_data.grade
        },
        session=session_maker
    )
    await state.set_state(ProfileUpdateStates.waiting_for_next_step)
    await callback_query.message.answer(
        text=TEXT_PROFILE_PARTIAL_UPDATE_SUCCESS,
        reply_markup=profile_next_step_keyboard()
    )


async def profile_partial_updater(
        message: types.Message,
        session_maker: sessionmaker,
        state: FSMContext):
    """
    Handler for update choose field (not grade!)
    :param message:
    :param session_maker:
    :param state:
    :return:
    """
    if message.text == "Отмена":
        await state.clear()
        return await start(message)

    field = (await state.get_data()).get("field")
    if user_field_validator(field, message.text):
        await update_user(
            user_id=message.from_user.id,
            fields={
                field: message.text
            },
            session=session_maker
        )

        await state.set_state(ProfileUpdateStates.waiting_for_next_step)
        return await message.answer(
            text=TEXT_PROFILE_PARTIAL_UPDATE_SUCCESS,
            reply_markup=profile_next_step_keyboard()
        )
    else:
        if field != "email":
            return await message.answer(TEXT_INVALID_EMAIL)
        else:
            return await message.answer(TEXT_INVALID_FIST_LASTNAME)


async def next_step_handler(
        callback_query: types.CallbackQuery,
        callback_data: NextStepCallBack,
        session_maker: sessionmaker,
        state: FSMContext,
):
    """
    Callback handler with next step button (return to main menu or go to continue editing
    :param callback_query:
    :param callback_data:
    :param session_maker:
    :param state:
    :return:
    """
    await state.clear()
    match callback_data.step:
        case "main":
            return await start(callback_query.message)

        case "editing":
            await profile_main(
                callback_query.message,
                session_maker=session_maker,
                state=state,
                from_user_id=callback_query.from_user.id
            )

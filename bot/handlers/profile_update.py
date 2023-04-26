import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.bot_messages import TEXT_PROFILE_PARTIAL_UPDATE
from bot.db import get_user, update_user
from bot.handlers.profile_create import profile_main
from bot.handlers.start import start
from bot.settings import NAME_REG_EXP, EMAIL_REG_EXP
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


async def profile_edit(callback_query: types.CallbackQuery, session_maker: sessionmaker, state: FSMContext):
    '''
    Partial editing user's profile
    :param callback_query:
    :param session_maker:
    :param state:
    :return:
    '''
    user = await get_user(callback_query.from_user.id, session=session_maker)
    await state.set_state(ProfileUpdateStates.waiting_for_choose_field)
    text = TEXT_PROFILE_PARTIAL_UPDATE.format(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        prof_role=user.professional_role,
        exp=user.grade
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
    '''
    Callback handler, return message with text about choose field
    :param callback_query:
    :param callback_data:
    :param state:
    :return:
    '''
    await state.set_state(ProfileUpdateStates.waiting_for_partial_update_data)
    await state.update_data(field=callback_data.field)
    cancel_board = cancel_keyboard()

    match callback_data.field:
        case "firstname":
            await callback_query.message.answer(
                "Пришлите своё имя",
                reply_markup=cancel_board
            )

        case "lastname":
            await callback_query.message.answer(
                "Пришлите свою фамилию",
                reply_markup=cancel_board
            )

        case "email":
            await callback_query.message.answer(
                "Пришлите свой email",
                reply_markup=cancel_board
            )

        case "professional_role":
            await callback_query.message.answer(
                "Пришлите свою специальность",
                reply_markup=cancel_board
            )

        case "grade":
            await callback_query.message.answer(
                "Выберите свой стаж",
                reply_markup=exp_type_keyboard()
            )

        case "cancel":
            return await start(callback_query.message)


async def profile_edit_grade(
        callback_query: types.CallbackQuery,
        callback_data: ExpTypeCallBack,
        session_maker: sessionmaker,
        state: FSMContext,
):
    '''
    Callback handler to update profile grade
    :param callback_query:
    :param callback_data:
    :param session_maker:
    :param state:
    :return:
    '''
    if callback_data.grade == 'cancel':
        await callback_query.message.answer('Создание профиля отменено')
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
        f'Данные успешно изменены. Куда дальше?',
        reply_markup=profile_next_step_keyboard()
    )


async def profile_partial_updater(
        message: types.Message,
        session_maker: sessionmaker,
        state: FSMContext):
    '''
    Handler for update choose field (not grade!)
    :param message:
    :param session_maker:
    :param state:
    :return:
    '''
    if message.text == 'Отмена':
        await state.clear()
        return await start(message)

    field = (await state.get_data()).get('field')
    if field in ("firstname", "lastname"):
        if re.match(NAME_REG_EXP, message.text):

            await update_user(
                user_id=message.from_user.id,
                fields={
                    field: message.text
                },
                session=session_maker
            )

            await state.set_state(ProfileUpdateStates.waiting_for_next_step)
            return await message.answer(f'Данные успешно изменены. Куда дальше?',
                                        reply_markup=profile_next_step_keyboard()
                                        )
        else:
            return await message.answer('Имя/ фамилия должны начинаться с заглавной буквы '
                                        'и не должны содержать цифр. Попробуйте ещё раз')
    if field == "email":
        if re.match(EMAIL_REG_EXP, message.text):

            await update_user(
                user_id=message.from_user.id,
                fields={
                    field: message.text
                },
                session=session_maker
            )

            await state.set_state(ProfileUpdateStates.waiting_for_next_step)
            return await message.answer(
                f'Данные успешно изменены. Куда дальше?',
                reply_markup=profile_next_step_keyboard()
            )
        else:
            await message.answer(
                text="Вы прислали невалидный email. Попробуйте ещё раз, н-р: example@test.com",
                reply_markup=cancel_keyboard()
            )
    else:
        await update_user(
            user_id=message.from_user.id,
            fields={
                field: message.text
            },
            session=session_maker
        )

        await state.set_state(ProfileUpdateStates.waiting_for_next_step)
        return await message.answer(f'Данные успешно изменены. Куда дальше?', reply_markup=profile_next_step_keyboard())


async def next_step_handler(
        callback_query: types.CallbackQuery,
        callback_data: NextStepCallBack,
        session_maker: sessionmaker,
        state: FSMContext,
):
    '''
    Callback handler with next step button (return to main menu or go to continue editing
    :param callback_query:
    :param callback_data:
    :param session_maker:
    :param state:
    :return:
    '''
    await state.clear()
    match callback_data.step:
        case 'main':
            return await start(callback_query.message)

        case 'editing':
            await profile_main(
                callback_query.message,
                session_maker=session_maker,
                state=state,
                from_user_id=callback_query.from_user.id
            )

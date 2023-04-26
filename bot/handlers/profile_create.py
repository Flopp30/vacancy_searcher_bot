import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import sessionmaker

from bot.bot_messages import TEXT_PROFILE_EDIT, TEXT_PROFILE_CREATE
from bot.db.user import is_user_exist, create_user
from bot.handlers.start import start
from bot.settings import EMAIL_REG_EXP, NAME_REG_EXP
from bot.structure import ProfileCreateStates, ProfileUpdateStates, ExpTypeCallBack
from bot.structure.keyboards import (
    profile_inline_menu,
    cancel_keyboard,
    exp_type_keyboard,
)


async def profile_main(
        message: types.Message,
        session_maker: sessionmaker,
        state: FSMContext,
        from_user_id: int = None
):
    '''
    Creating and editing user's profile
    :param message:
    :param session_maker:
    :param state:
    :param from_user_id:
    :return:
    '''
    user_id = from_user_id if from_user_id else message.from_user.id
    if await is_user_exist(user_id, session_maker):
        text = TEXT_PROFILE_EDIT
        await state.set_state(ProfileUpdateStates.waiting_for_choose_edit_type)
    else:
        text = TEXT_PROFILE_CREATE
        await state.set_state(ProfileCreateStates.waiting_for_choose_create_type)
    await message.answer(text=text, reply_markup=profile_inline_menu())


async def profile_create_firstname(
        callback_query: types.CallbackQuery,
        state: FSMContext
):
    '''
    Creating and editing user's firstname
    :param callback_query:
    :param state:
    :return:
    '''
    await state.set_state(ProfileCreateStates.waiting_for_firstname)
    await callback_query.message.answer(text="Пришлите своё имя", reply_markup=cancel_keyboard())


async def profile_create_lastname(
        message: types.Message,
        state: FSMContext
):
    '''
    Creating user's lastname
    :param message:
    :param state:
    :return:
    '''
    if message.text == 'Отмена':
        await message.answer('Создание профиля отменено')
        await state.clear()
        return await start(message)
    elif re.match(NAME_REG_EXP, message.text):
        await state.update_data(firstname=message.text)
        await state.set_state(ProfileCreateStates.waiting_for_lastname)
        await message.answer(text="Пришлите свою фамилию", reply_markup=cancel_keyboard())
    else:
        await message.answer('Имя должно начинаться с заглавной буквы '
                             'и не должно содержать цифр. Попробуйте ещё раз')


async def profile_create_email(message: types.Message, state: FSMContext):
    '''
    Creating user's email
    :param message:
    :param state:
    :return:
    '''
    if message.text == 'Отмена':
        await message.answer('Создание профиля отменено')
        await state.clear()
        return await start(message)
    elif re.match(NAME_REG_EXP, message.text):
        await state.update_data(lastname=message.text)
        await state.set_state(ProfileCreateStates.waiting_for_email)
        await message.answer(text="Пришлите email", reply_markup=cancel_keyboard())
    else:
        await message.answer('Фамилия должна начинаться с заглавной буквы '
                             'и не должна содержать цифр. Попробуйте ещё раз')


async def profile_create_professional(message: types.Message, state: FSMContext):
    '''
    Creating user's prof role
    :param message:
    :param state:
    :return:
    '''
    if message.text == 'Отмена':
        await message.answer('Создание профиля отменено')
        await state.clear()
        return await start(message)
    elif re.match(EMAIL_REG_EXP, message.text):
        await state.update_data(email=message.text)
        await state.set_state(ProfileCreateStates.waiting_for_professional_role)
        await message.answer(text="Пришлите название своей профессии", reply_markup=cancel_keyboard())
    else:
        await message.answer(
            text="Вы прислали невалидный email. Попробуйте ещё раз, н-р: example@test.com",
            reply_markup=cancel_keyboard()
        )


async def profile_create_experience(
        message: types.Message,
        state: FSMContext
):
    '''
    Creating user's exp
    :param message:
    :param state:
    :return:
    '''
    if message.text == 'Отмена':
        await message.answer('Создание профиля отменено')
        await state.clear()
        return await start(message)
    await state.update_data(professional_role=message.text)
    await state.set_state(ProfileCreateStates.waiting_for_experience)
    await message.answer(text="Пришлите опыт работы", reply_markup=exp_type_keyboard())


async def profile_create_end(
        callback_query: types.CallbackQuery,
        callback_data: ExpTypeCallBack,
        session_maker: sessionmaker,
        state: FSMContext
):
    '''
    End creating and editing
    :param callback_query:
    :param callback_data:
    :param session_maker:
    :param state:
    :return:
    '''
    if callback_data.grade == 'cancel':
        await callback_query.message.answer('Создание профиля отменено')
        return await start(callback_query.message)
    data = await state.get_data()
    user_args = {
        'user_id': callback_query.from_user.id,
        'firstname': data.get('firstname', None),
        'lastname': data.get('lastname', None),
        'email': data.get('email', None),
        'professional_role': data.get('professional_role', None),
        'grade': callback_data.grade,
    }
    await create_user(session=session_maker, **user_args)
    await state.clear()
    await callback_query.message.answer(text=f"Спасибо, данные успешно сохранены")
    await start(callback_query.message)

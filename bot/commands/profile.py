from aiogram import types


async def profile(message: types.Message):
    return message.answer(text="Здесь будет профиль / резюме в вэбе")
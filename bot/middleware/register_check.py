from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker

from bot.db import is_user_exist, create_user, GradeTypes


class RegisterCheck(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        if not await is_user_exist(user_id=event.from_user.id, session=session_maker):
            await create_user(
                user_id=event.from_user.id,
                firstname='Artem',
                professional_role="Python dev",
                grade=GradeTypes.MIDDLE,
                email="pospeev.artem@icloud.com",
                session=session_maker,
            )

            if isinstance(event, Message):
                await event.answer("Профиль успешно создан")
            else:
                await event.message.answer("Профиль успешно создан")

        return await handler(event, data)

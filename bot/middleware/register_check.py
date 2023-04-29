"""
Create new user after start chatting
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm import sessionmaker

from bot.db import create_user, User, is_object_exist


class RegisterCheck(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        session_maker: sessionmaker = data["session_maker"]
        if not await is_object_exist(object_=User, id_=event.from_user.id, session=session_maker):
            await create_user(
                user_id=event.from_user.id,
                session=session_maker,
            )

        return await handler(event, data)

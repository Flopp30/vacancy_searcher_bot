"""
Create new user after start chatting
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from db.crud.base import user_crud


class RegisterCheck(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:

        user = await user_crud.get_by_attribute(
            attr_name='id',
            attr_value=event.from_user.id,
            is_deleted=False)
        if not user:
            await user_crud.create({'id': event.from_user.id})

        return await handler(event, data)

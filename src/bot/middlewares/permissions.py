from typing import Any, Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.structures.data_structure import TransferDataWithEngine
from bot.structures.role import Role


class PermissionMiddleware(BaseMiddleware):

    def __init__(self, handler_role: Role):
        self.handler_role: Role= handler_role

    async def __call__(
            self,
            handler: Callable[[TelegramObject, TransferDataWithEngine], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: TransferDataWithEngine
    ) -> Any:
        data['role'] = await data['db'].user.get_role(user_id=event.from_user.id)

        if data['role'] >= self.handler_role:
            return await handler(event, data)

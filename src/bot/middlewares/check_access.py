from typing import Any, Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject, User

from bot.structures.data_structure import TransferDataWithEngine
from db.database import Database


class CheckAccessMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, TransferDataWithEngine], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: TransferDataWithEngine
    ) -> Any:

        user = data['event_from_user']
        data['user'] = await self.register_if_not_exist(user, data['db'])
        return await handler(event, data)

    async def register_if_not_exist(self, user: User, db: Database):

        current_user = await db.user.get_by_user_id(user_id=user.id)

        if current_user is None:
            current_user = await db.user.new(
                user_id=user.id,
                user_name=user.username,
                first_name=user.first_name, 
                second_name=user.last_name,
                is_premium=bool(user.is_premium)
            )

            await db.session.commit()
        return current_user

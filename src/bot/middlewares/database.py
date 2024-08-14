from typing import Any, Awaitable, Callable, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.structures.data_structure import TransferDataWithEngine
from db.database import Database



class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler."""

    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], TransferDataWithEngine], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: TransferDataWithEngine 
    ) -> Any:
        """This method calls every update."""
        async with AsyncSession(bind=data['engine']) as session:
            data['db'] = Database(session)
            return await handler(event, data)

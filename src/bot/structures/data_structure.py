"""Data Structures.

This file contains TypedDict structure to store data which will
transfer throw Dispatcher->Middlewares->Handlers.
"""

from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine

from bot.structures.role import Role
from db.database import Database
from db.models.user import User


class TransferData(TypedDict):
    """Common transfer data."""

    bot: Bot
    db: Database
    role: Role
    user: User


class TransferDataWithEngine(TransferData):
    engine: AsyncEngine

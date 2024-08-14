from typing import Optional

from aiogram import Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from bot.handlers import routers
from bot.middlewares.database import DatabaseMiddleware
from bot.middlewares.check_access import CheckAccessMiddleware


def get_dispatcher(
    storage: BaseStorage = MemoryStorage(),
    fsm_strategy: Optional[FSMStrategy] = FSMStrategy.CHAT,
    event_isolation: Optional[BaseEventIsolation] = None,
):
    """This function set up dispatcher with routers, filters and middlewares"""
    dp = Dispatcher(
        storage=storage
    )

    # Register middlewares
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(CheckAccessMiddleware())

    setup_dialogs(dp)

    for router in routers:
        dp.include_router(router)


    return dp

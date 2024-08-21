from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import  Message
from aiogram_dialog import DialogManager, StartMode

from .dialogs import main_dialog
from bot.handlers.bebris.main.dialogs import bebris_dialog
from bot.handlers.bebris.repitition.dialogs import bebris_train_dialog
from bot.states import MainSG


router = Router()


router.include_router(main_dialog)
router.include_router(bebris_dialog)
router.include_router(bebris_train_dialog)


@router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        MainSG.start,
        mode=StartMode.RESET_STACK,
    )

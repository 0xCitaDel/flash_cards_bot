from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.widgets.kbd import Button

from bot.states import BebrisDialogSG, MainSG


async def bebris_dialog_start(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager
    ):
    await manager.start(
        BebrisDialogSG.start, 
        # show_mode=ShowMode.DELETE_AND_SEND
    )

async def main_menu(
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager
    ):
    await manager.start(
        MainSG.start,
        mode=StartMode.RESET_STACK,
    )

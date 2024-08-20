from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def go_back(
        callback: CallbackQuery,
        widjet: Button,
        dialog_manager: DialogManager
    ):
    await dialog_manager.back()


async def close_dialog(
        callback: CallbackQuery,
        widget: Button,
        dialog_manager: DialogManager
    ):
    await dialog_manager.done()

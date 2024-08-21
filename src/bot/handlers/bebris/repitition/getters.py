from aiogram_dialog import DialogManager, ShowMode

from db.database import Database
from services import BebrisService

async def repeat_lesson_getter(dialog_manager: DialogManager, **kwargs):
    lessons = dialog_manager.start_data['lessons']
    return {'lessons': lessons}

async def initialize_lesson_getter(dialog_manager: DialogManager, **kwargs):
    flash_cards = dialog_manager.dialog_data['flash_cards']
    return {'flash_cards': flash_cards}

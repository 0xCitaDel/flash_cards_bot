from operator import le
import random

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bot.states import BebrisDialogSG, BebrisTrainDialogSG
from db.database import Database
from services.bbr_repitition import RepititionService

async def select_repeat_lessons(
    callback: CallbackQuery,
    widget: Button,
    manager: DialogManager
):
    """
    Some here...
    """
    db: Database = manager.middleware_data['db']
    user_id = manager.middleware_data['user'].id

    lessons = await RepititionService(db).get_repitition_lessons(user_id)

    await manager.start(
        BebrisTrainDialogSG.repeat_lessons_list,
        data={'lessons': lessons}
    )


async def initialize_lesson(callback: CallbackQuery, widget: Select,
                       manager: DialogManager, item_id):
    """
    some here later...
    """
    db: Database = manager.middleware_data['db']
    user_id = manager.middleware_data['user'].id

    index = int(item_id) - 1
    lesson = manager.start_data['lessons'][index]

    playlist_id = lesson['playlist_id']
    lesson_id = lesson['lesson_id']

    flash_cards = await RepititionService(db).get_repitition_cards(
        user_id= user_id, playlist_id = playlist_id, lesson_id=lesson_id
    )

    manager.dialog_data['flash_cards'] = flash_cards
    await manager.switch_to(BebrisTrainDialogSG.initialize_lesson)

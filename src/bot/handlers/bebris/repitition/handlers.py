from operator import le
import random

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bot.states import BebrisTrainDialogSG
from db.database import Database
from services.bbr_repitition import RepititionService

class RepititionBebrisHandler:

    async def select_repeat_lessons(
        self,
        callback: CallbackQuery,
        widget: Button,
        manager: DialogManager
    ):
        """
        TODO: Some here...
        """
        db: Database = manager.middleware_data['db']
        user_id = manager.middleware_data['user'].id

        lessons = await RepititionService(db).get_repitition_lessons(user_id)

        await manager.start(
            BebrisTrainDialogSG.repeat_lessons_list,
            data={'lessons': lessons}
        )

    async def initialize_lesson(self, callback: CallbackQuery, widget: Select,
                           manager: DialogManager, item_id):
        """
        TODO: some here later...
        """
        db: Database = manager.middleware_data['db']
        user_id = manager.middleware_data['user'].id

        # Get the lesson based on the index in the list of lessons
        index = int(item_id) - 1
        lesson = manager.start_data['lessons'][index]

        playlist_id = lesson['playlist_id']
        lesson_id = lesson['lesson_id']

        flash_cards = await RepititionService(db).get_repitition_cards(
            user_id= user_id, playlist_id = playlist_id, lesson_id=lesson_id
        )
        manager.dialog_data['flash_cards'] = flash_cards

        # Set the default radio button selection for the lesson mode
        await manager.find('radio_reverse_mode').set_checked(item_id='0')

        await manager.switch_to(BebrisTrainDialogSG.initialize_lesson)

    async def initialize_all_lessons(self, callback: CallbackQuery, widget: Button,
                           manager: DialogManager):
        """
        TODO: some here later...
        """
        db: Database = manager.middleware_data['db']
        user_id = manager.middleware_data['user'].id

        flash_cards = await RepititionService(db).get_repitition_all_cards(
            user_id= user_id
        )
        manager.dialog_data['flash_cards'] = flash_cards

        # Set the default radio button selection for the lesson mode
        await manager.find('radio_reverse_mode').set_checked(item_id='0')

        await manager.switch_to(BebrisTrainDialogSG.initialize_lesson)

    async def start_repitition_session(self, callback: CallbackQuery,
                         widget: Button, manager: DialogManager):
        """
        Handler shuffle and switches the state to start playing flashcards.
        """
        # Remove existing lesson data from the dialog context
        manager.dialog_data.pop('lessons', None)
        db = manager.middleware_data['db']

        data = await RepititionService(db).create_dialog_data(manager)
        manager.dialog_data.update(data)

        all_cards = manager.dialog_data['all_cards']
        random.shuffle(all_cards)

        await manager.switch_to(BebrisTrainDialogSG.next_card)

    async def next_card_or_completion(self,callback: CallbackQuery,
                                      widget: Button, manager: DialogManager):
        """
        Handles the transition to the next flashcard or completes the lessons
        if all cards have been reviewed.
        """ 
        # Retrieve dialog data and database connection
        data = manager.dialog_data
        db: Database = manager.middleware_data['db']

        # Get the current card index and its ID
        index_current_card = data['current_card_index']
        current_card = data['all_cards'][index_current_card]

       # Process the user's choice: correct or incorrect
        if widget.widget_id == 'correct':
            await self._process_correct_answer(db, current_card, data)
        else:
            await self._process_wrong_answer(db, current_card,data)

        await self._move_to_next_card_or_finish(db, manager, data)

    async def _process_correct_answer(self, db: Database, current_card: dict, data: dict):
        card_id = current_card['flashcard_id']
        data['correct_answer_ids'].append(card_id)

        correct_count = current_card['correct_count'] + 1

        repitition_service = RepititionService(db)

        if correct_count >= 3:
            await repitition_service.delete_flashcard_stat(card_id)
        else:
            await repitition_service.update_flashcard_stat(card_id, correct_count, True)

    async def _process_wrong_answer(self, db: Database, current_card: dict, data: dict):
        card_id = current_card['flashcard_id']
        data['wrong_answer_ids'].append(card_id)

        correct_count = max(current_card['correct_count']- 1, 0)

        repitition_service = RepititionService(db) 
        await repitition_service.update_flashcard_stat(card_id, correct_count, False)
    
    async def _move_to_next_card_or_finish(self, db: Database, manager: DialogManager, data: dict):

        # Increment the current card index to move to the next one   
        data['current_card_index'] += 1

        # Update flashcard data in the dialog_data
        data_update = await RepititionService(db).update_flashcards_data(data)
        data.update(data_update)

        # Check if there are more cards to review
        if data['current_card_index'] < data['total_cards']:
            await manager.switch_to(BebrisTrainDialogSG.next_card)
        else:
            await manager.switch_to(BebrisTrainDialogSG.results)
        pass

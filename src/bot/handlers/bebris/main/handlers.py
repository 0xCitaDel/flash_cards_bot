import random

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bot.states import BebrisDialogSG, BebrisTrainDialogSG
from db.database import Database
from services.bbr_cards import BebrisService


class MainBebrisHandler:

    async def select_lesson(self, callback: CallbackQuery, widget: Select,
                            manager: DialogManager, item_id):
        """
        Handler switches the state to select the lesson number

        :param item_id: playlist primary key (playlist ID)
        """
        # Extract the database and user information from the middleware data
        db = manager.middleware_data['db']
        user_id = manager.middleware_data['user'].id

        # Store the selected playlist ID in the dialog data as an integer
        manager.dialog_data['playlist_id'] = int(item_id)

        # Fetch the lessons and store them in dialog data
        manager.dialog_data['lessons'] = await BebrisService(db).get_lessons(
            user_id=user_id,
            playlist_id=manager.dialog_data['playlist_id']
        )

        # Transition to the lesson selection state
        await manager.switch_to(BebrisDialogSG.choice_lesson)

    async def initialize_lesson(self, callback: CallbackQuery, widget: Select,
                                manager: DialogManager, item_id):
        """
        Initializes the lesson based on the item selected by the user

        :param item_id: lesson primary key (lesson ID)
        """
        await self._initialize_lesson_data(manager, int(item_id))

    async def initialize_lesson_from_input(self, message: Message,
                                           widget: ManagedTextInput,
                                           manager: DialogManager, text: str):
        """
        Initializes the lesson based on the lesson number entered by the user

        :param text: lesson primary key (lesson ID)
        """
        lessons_count = len(manager.dialog_data['lessons'])
        
        # Validate the entered lesson number
        if not self.__validate_lesson_number(text, lessons_count):
            return await message.answer(
                f'⛔️ Введен недопустимый номер урока.'
                f' Пожалуйста, укажите значение от 1 до {lessons_count} ⛔️'
            )
        
        item_id = manager.dialog_data['lessons'][int(text)-1]['id']
        # If the lesson number is valid, initialize the lesson
        await self._initialize_lesson_data(manager, item_id)

    async def show_all_cards(self, callback: CallbackQuery,
                             widget: Button, manager: DialogManager):
        """
        Handler for showing all flashcards
        """
        await manager.switch_to(BebrisDialogSG.show_all_cards)

    async def start_flashcard_session(self, callback: CallbackQuery,
                         widget: Button, manager: DialogManager):
        """
        Handler shuffle and switches the state to start playing flashcards.
        """
        # Remove existing lesson data from the dialog context
        manager.dialog_data.pop('lessons', None)

        all_cards = manager.dialog_data['all_cards']
        random.shuffle(all_cards)
        await manager.switch_to(BebrisDialogSG.next_card)

    async def next_card_or_completion(self, callback: CallbackQuery,
                                      widget: Button, manager: DialogManager):
        """
        Handles the transition to the next flashcard or completes the lessons
        if all cards have been reviewed.
        """ 
        # Retrieve dialog data and database connection
        data = manager.dialog_data
        db = manager.middleware_data['db']

        # Get the current card index and its ID
        index_current_card = data['current_card_index']
        card_id = data['all_cards'][index_current_card][0]

        # Process the user's choice: correct or incorrect
        if widget.widget_id == 'correct':
            data['correct_answer_ids'].append(card_id)
        else:
            data['wrong_answer_ids'].append(card_id)

        # Increment the current card index to move to the next one   
        data['current_card_index'] += 1

        # Update flashcard data in the dialog_data
        data_update = await BebrisService(db).update_flashcards_data(data)
        data.update(data_update)

        # Check if there are more cards to review
        if data['current_card_index'] < data['total_cards']:
            await manager.switch_to(BebrisDialogSG.next_card)
        else:
            user_id = manager.middleware_data['user'].id
            await BebrisService(db).save_lesson_result(user_id, data)

            await manager.switch_to(BebrisDialogSG.conclusion)

    async def lesson_exit(self, callback: CallbackQuery,
                          widget: Button, manager: DialogManager):
        """
        Handler for exiting the lesson
        """
        await manager.switch_to(BebrisDialogSG.lesson_exit)

    async def _initialize_lesson_data(
        self,
        manager: DialogManager,
        item_id: int
    ):
        """
        Prepares the lesson start by showing introductory info
        before flashcard review begins.

        :param item_id: lesson primary key (lesson ID)
        """

        # Fetch lesson data and flashcards from the database and update the context
        db: Database = manager.middleware_data['db']
        bebris_service = BebrisService(db)
        data: dict = await bebris_service.get_cards_and_create_dialog_data(
            lesson_id=item_id
        )
        manager.dialog_data.update(data)         

        # Set the default radio button selection for the lesson mode
        await manager.find('radio_reverse_mode').set_checked(item_id='0')

        # Transition to the lesson preparation state
        await manager.switch_to(BebrisDialogSG.preparation)

    def __validate_lesson_number(self, text: str, lesson_count) -> bool:
        if all(ch.isdigit() for ch in text) and 1 <= int(text) <= lesson_count:
            return True
        return False

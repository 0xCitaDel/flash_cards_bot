import random as rand
from collections.abc import Sequence

from aiogram_dialog import DialogManager

from db.database import Database
from db.models.bbr_models.flash_card import FlashCardBebris
from db.models.bbr_models.lesson import LessonBebris
from db.models.bbr_models.playlist import PlaylistBebris

class RepititionService:
    db: Database

    def __init__(self, db) -> None:
        self.db: Database = db

    async def get_repitition_lessons(self, user_id: int):
        """
        This function returns a list of lessons that the user needs to repeat.
        The result of this function is passed to the start_data of dialog_manager.

        Arguments:
            user_id (int): The ID of the user.

        Returns:
            data (list): A list of dictionaries with data about each lesson.
        """
        lessons = await self.db.bbr_flash_card_statistic.get_lessons_by_user_id(user_id)

        # Check if there are no lessons to repeat
        if not lessons:
            return []

        data = [
            {
                'position'      : pos + 1,
                'playlist_id'   : lesson_data.playlist_id,
                'lesson_id'     : lesson_data.lesson_id,
                'emoji'         : lesson_data.emoji,
                'playlist_name' : lesson_data.playlist_name,
                'lesson_title'  : lesson_data.lesson_title,
                'lesson_number' : lesson_data.lesson_number,
                'video_number'  : lesson_data.video_number,
                'card_count'    : lesson_data.card_count
            }
            for pos, lesson_data in enumerate(lessons)
        ]
        return data

    async def get_repitition_cards(self, user_id: int, playlist_id: int, lesson_id: int):
        """
        Fetches flashcards for a specific lesson that the user needs to repeat.
        The result is passed to dialog_data.

        Arguments:
            user_id (int): The ID of the user.
            playlist_id (int): The ID of the playlist.
            lesson_id (int): The ID of the lesson.

        Returns:
            data (list): A list of dictionaries containing flashcard data.
        """ 
        flash_cards = await self.db.bbr_flash_card_statistic.get_flashcards(
            user_id=user_id,
            playlist_id=playlist_id,
            lesson_id=lesson_id
        )

        data = [
            {
                'position'      : pos + 1,
                'flashcard_id'  : card.flashcard_id,
                'front_side'    : card.front_side,
                'back_side'     : card.back_side,
                'correct_count' : card.correct_count,
                'last_result'   : card.last_result
            }
            for pos, card in enumerate(flash_cards)
        ]
        return data

    async def get_repitition_all_cards(self, user_id: int):
        """
        Fetches flashcards for a specific lesson that the user needs to repeat.
        The result is passed to dialog_data.

        Arguments:
            user_id (int): The ID of the user.

        Returns:
            data (list): A list of dictionaries containing flashcard data.
        """ 
        flash_cards = await self.db.bbr_flash_card_statistic.get_all_flashcards(
            user_id=user_id
        )

        data = [
            {
                'position'      : pos + 1,
                'flashcard_id'  : card.flashcard_id,
                'front_side'    : card.front_side,
                'back_side'     : card.back_side,
                'correct_count' : card.correct_count,
                'last_result'   : card.last_result
            }
            for pos, card in enumerate(flash_cards)
        ]
        return data

    async def create_dialog_data(self, manager: DialogManager):
        """
        Prepares and returns the initial dialog data for the lesson session.
        The result is passed to dialog_data in the dialog manager.

        Returns:
        dict: A dictionary containing information about the current card, lesson, 
          and statistical data for tracking the session progress.
        """
        flash_cards = manager.dialog_data['flash_cards']

        return {
            # Information about the current card and lesson
            'current_card_id'       : None,
            'current_card_index'    : 0,
            'front_text'            : None,
            'back_text'             : None,
            'position'              : 1,
            'all_cards'             : flash_cards,

            # Statistical data for the session
            'total_cards'           : len(flash_cards),
            'total_correct_answers' : 0,
            'total_wrong_answers'   : 0,
            'accuracy_percent'      : 100,

            # Lists for tracking correct and incorrect answers
            'correct_answer_ids'    : [],
            'wrong_answer_ids'      : []
        }

    async def update_flashcards_data(self, data: dict) -> dict:
        """
        Updates flashcards data and calculates the accuracy percentage.

        :param data: Dictionary containing current dialog_data.
        :return: Updated data dictionary with the current card's information.
        """
        index = data['current_card_index']
        accuracy = self._get_accuracy_percentage(
            index_current_card=index,
            total_correct_card=len(data['correct_answer_ids'])
        )

        if index < data['total_cards']:
            return self._prepare_current_card_data(data, index, accuracy)
        return {'accuracy_percent': accuracy}

    def _prepare_current_card_data(
        self,
        data: dict,
        index: int,
        accuracy: float
    ) -> dict:
        """
        Prepares data for the current card to be shown.

        :param data: Dictionary containing current session data.
        :param index: The index of the current card.
        :param accuracy: The calculated accuracy percentage.
        :return: A dictionary with the current card's data and statistics.
        """
        current_card = data['all_cards'][index]
        mode = int(data['reverse_mode'])

        return {
            'current_card_id': current_card['flashcard_id'],
            'position': data['position'] + 1,
            'accuracy_percent': accuracy,
            'front_text': current_card['front_side' if mode else 'back_side'],
            'back_text': current_card['back_side' if mode else 'front_side'],
            'total_cards': data['total_cards'],
            'total_correct_answers': len(data['correct_answer_ids']),
            'total_wrong_answers': len(data['wrong_answer_ids']),
        }

    def _get_accuracy_percentage(
        self, index_current_card: int, total_correct_card: int
    ) -> int:
        """
        Calculates the accuracy percentage based on the current index 
        and correct answers.

        :param index_current_card: The index of the current card.
        :param total_correct_card: The total number of correct answers.
        :return: The accuracy percentage as a integer.
        """
        if index_current_card == 0:
            return 100
        return int(total_correct_card / index_current_card * 100)

    async def delete_flashcard_stat(self, card_id: int):
        await self.db.bbr_flash_card_statistic.delete_by_card_id(card_id)
        await self.db.session.commit()

    async def update_flashcard_stat(self, card_id: int, correct_count: int, last_result: bool):
        await self.db.bbr_flash_card_statistic.update_by_card_id(
            flashcard_id=card_id,
            correct_count = correct_count,
            last_result=last_result
        )
        await self.db.session.commit()

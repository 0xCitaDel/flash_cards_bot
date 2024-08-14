from collections.abc import Sequence
from db.database import Database
from db.models.bbr_models.flash_card import FlashCardBebris
from db.models.bbr_models.lesson import LessonBebris
from db.models.bbr_models.playlist import PlaylistBebris


class BebrisService:
    db: Database

    def __init__(self, db) -> None:
        self.db: Database = db

    async def get_playlists(self) -> list:
        """
        Retrieve all playlists from the database.

        :return: A list of tuples with playlist details (id, name, emoji, color).
        """
        playlists: Sequence[PlaylistBebris] = await self.db.bbr_playlist.get_all()
        playlist_items = [
            (i.id, i.playlist_name, i.emoji, i.playlist_color)
            for i in playlists
        ]
        return playlist_items

    async def get_lessons(self, playlist_id: int) -> list:
        """
        Retrieve all lessons for a specific playlist.

        :param playlist_id: The ID of the playlist.
        :return: A list of tuples with lesson details (id, title).
        """
        lessons: Sequence[LessonBebris] = await self.db.bbr_lesson.get_by_playlist_id(
            playlist_id=playlist_id
        )
        lesson_items = [(i.id, i.lesson_title) for i in lessons]
        return lesson_items

    async def get_cards_and_create_dialog_data(self, lesson_id: int) -> dict:
        """
        Retrieve all flashcards for a lesson and prepare initial dialog data.

        :param lesson_id: The ID of the lesson.
        :return: A dictionary containing the initial state for the dialog.
        """
        cards: Sequence[FlashCardBebris] = await self.db.bbr_flash_card.get_by_lesson_id(
            lesson_id=lesson_id
        )
        all_cards = [(i.id, i.front_side, i.back_side) for i in cards]

        return {
            # Information about the current card and lesson
            'current_card_id': None,
            'current_card_index': 0,
            'front_text': None,
            'back_text': None,
            'position': 1,
            'lesson_id': lesson_id,
            'all_cards': all_cards,

            # Statistical data for the session
            'total_cards': len(all_cards),
            'total_correct_answers': 0,
            'total_wrong_answers': 0,
            'accuracy_percent': 100,

            # Lists for tracking correct and incorrect answers
            'correct_answer_ids': [],
            'wrong_answer_ids': []
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

    async def save_lesson_result(self, user_id: int, data: dict):
        await self.db.bbr_lesson_statistic.new(
            user_id=user_id,
            lesson_id=data['lesson_id'],
            correct_answers=len(data['correct_answer_ids']),
            wrong_answers=len(data['wrong_answer_ids']),
            accuracy=data['accuracy_percent']
        )
        await self.db.session.commit()

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
            'current_card_id': current_card[0],
            'position': data['position'] + 1,
            'accuracy_percent': accuracy,
            'front_text': current_card[1 if mode else 2],
            'back_text': current_card[2 if mode else 1],
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

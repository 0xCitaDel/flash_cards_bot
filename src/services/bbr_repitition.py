import random as rand
from collections.abc import Sequence

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
        some here later...
        """
        lessons = await self.db.bbr_flash_card_statistic.get_lessons_by_user_id(user_id)
        data = [
            {
                'position': pos + 1,
                'playlist_id': i.playlist_id,
                'lesson_id': i.lesson_id,
                'emoji': i.emoji,
                'playlist_name': i.playlist_name,
                'lesson_title': i.lesson_title,
                'lesson_number': i.lesson_nubmer,
                'video_number': i.video_nubmer,
                'card_count': i.card_count
            }
            for pos, i in enumerate(lessons)
        ]
        return data

    async def get_repitition_cards(self, user_id: int, playlist_id: int, lesson_id: int):

        flash_cards = await self.db.bbr_flash_card_statistic.get_flashcards(
            user_id=user_id,
            playlist_id=playlist_id,
            lesson_id=lesson_id
        )

        data = [
            {
                'position': pos + 1,
                'flashcard_id': i.flashcard_id,
                'front_side': i.front_side,
                'back_side': i.back_side,
                'correct_count': i.correct_count,
                'last_result': i.last_result
            }
            for pos, i in enumerate( flash_cards)
        ]
        return data

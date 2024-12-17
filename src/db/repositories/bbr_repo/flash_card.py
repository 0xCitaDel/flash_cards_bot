from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from db.models.bbr_models import FlashCardBebris
from db.models.bbr_models.flash_card import FlashCardStatisticBebris
from db.models.bbr_models.lesson import LessonBebris
from db.models.bbr_models.playlist import PlaylistBebris
from db.repositories.abstract import AbstractRepository


class FlashCardBebrisRepo(AbstractRepository[FlashCardBebris]):
    """Lesosn repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=FlashCardBebris, session=session)

    async def get_by_lesson_id(self, lesson_id):
        result = await self.get_by_where(
            FlashCardBebris.lesson_id==lesson_id
        )
        return result.all()


class FlashCardStatisticBebrisRepo(AbstractRepository[FlashCardStatisticBebris]):
    """Lesosn repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=FlashCardStatisticBebris, session=session)

    async def delete_by_card_id(self, flashcard_id: int):
        statement = delete(self.type_model).where(self.type_model.flashcard_id==flashcard_id)
        await self.session.execute(statement)

    async def update_by_card_id(self,  flashcard_id: int, correct_count: int, last_result: bool):
        statement = update(self.type_model).where(self.type_model.flashcard_id == flashcard_id)\
            .values(
                correct_count = correct_count,
                last_result = last_result
            )
        await self.session.execute(statement)

    async def get_flashcards(self, user_id: int, playlist_id: int, lesson_id: int):
        query = (
            select(
                FlashCardStatisticBebris.flashcard_id,
                FlashCardBebris.front_side,
                FlashCardBebris.back_side,
                FlashCardStatisticBebris.correct_count,
                FlashCardStatisticBebris.last_result,
            )
            .join(
                FlashCardBebris,
                FlashCardStatisticBebris.flashcard_id == FlashCardBebris.id
            )
            .where(
                FlashCardStatisticBebris.user_id == user_id,
                FlashCardStatisticBebris.playlist_id==playlist_id,
                FlashCardStatisticBebris.lesson_id==lesson_id
            )

        ) 
        return (await self.session.execute(query)).all()

    async def get_all_flashcards(self, user_id: int):
        query = (
            select(
                FlashCardStatisticBebris.flashcard_id,
                FlashCardBebris.front_side,
                FlashCardBebris.back_side,
                FlashCardStatisticBebris.correct_count,
                FlashCardStatisticBebris.last_result,
            )
            .join(
                FlashCardBebris,
                FlashCardStatisticBebris.flashcard_id == FlashCardBebris.id
            )
            .where(FlashCardStatisticBebris.user_id == user_id)
        )

        return (await self.session.execute(query)).all()

    async def get_lessons_by_user_id(self, user_id: int):
        query = (
            select(
                FlashCardStatisticBebris.playlist_id,
                FlashCardStatisticBebris.lesson_id,
                PlaylistBebris.emoji,
                PlaylistBebris.playlist_name,
                LessonBebris.lesson_title,
                LessonBebris.lesson_number,
                LessonBebris.video_number,
                func.count(FlashCardStatisticBebris.flashcard_id).label('card_count')
            )
            .join(
                PlaylistBebris,
                FlashCardStatisticBebris.playlist_id == PlaylistBebris.id
            )
            .join(
                LessonBebris,
                FlashCardStatisticBebris.lesson_id == LessonBebris.id
            )
            .filter(
                FlashCardStatisticBebris.user_id == user_id
            )
            .group_by(
                FlashCardStatisticBebris.playlist_id,
                FlashCardStatisticBebris.lesson_id,
                PlaylistBebris.emoji,
                PlaylistBebris.playlist_name,
                LessonBebris.lesson_title,
                LessonBebris.lesson_number,
                LessonBebris.video_number
            )
        )
        return (await self.session.execute(query)).all()

    async def new(
            self,
            user_id: int,
            playlist_id: int,
            lesson_id: int,
            flashcard_ids: list,
            correct_count: int,
            last_result: bool,
    ) -> None:
        result = await self.get_by_where(
            FlashCardStatisticBebris.lesson_id==lesson_id
        )
        old_cards = [i.flashcard_id for i in result.all()]
        new_cards = list(set(flashcard_ids) - set(old_cards))
        for card_id in new_cards:
            self.session.add(
                FlashCardStatisticBebris(
                    user_id=user_id,
                    playlist_id=playlist_id,
                    lesson_id=lesson_id,
                    flashcard_id=card_id,
                    correct_count=correct_count,
                    last_result=last_result,
                )
            )

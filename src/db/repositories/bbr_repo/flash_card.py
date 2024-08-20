from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bbr_models import FlashCardBebris
from db.models.bbr_models.flash_card import FlashCardStatisticBebris
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

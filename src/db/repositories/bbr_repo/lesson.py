from collections.abc import Sequence
from typing import Optional

from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bbr_models import LessonBebris, LessonStatisticBebris
from db.repositories.abstract import AbstractRepository


class LessonBebrisRepo(AbstractRepository[LessonBebris]):
    """Lesosn repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=LessonBebris, session=session)

    
    async def get_by_playlist_id(self, playlist_id) -> Sequence[LessonBebris]:
        result = await self.get_by_where(
            LessonBebris.playlist_id==playlist_id
        )
        return result.all()


class LessonStatisticBebrisRepo(AbstractRepository[LessonStatisticBebris]):
    """Lesosn repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=LessonStatisticBebris, session=session)

    async def new(
            self,
            user_id: int,
            lesson_id: int,
            correct_answers: int,
            wrong_answers: int,
            accuracy: int,
    ) -> None:
        await self.session.merge(
            LessonStatisticBebris(
                user_id=user_id,
                lesson_id=lesson_id,
                correct_answers=correct_answers,
                wrong_answers=wrong_answers,
                accuracy=accuracy
            )
        )

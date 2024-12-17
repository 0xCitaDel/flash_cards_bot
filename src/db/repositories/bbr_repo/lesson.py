from collections.abc import Sequence
from typing import Optional

from sqlalchemy import  select, ScalarResult
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bbr_models import LessonBebris, LessonStatisticBebris
from db.repositories.abstract import AbstractRepository


class LessonBebrisRepo(AbstractRepository[LessonBebris]):
    """Lesosn repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=LessonBebris, session=session)

    
    async def get_lessons_with_statistics(self, playlist_id, user_id):
        subquery = select(
            LessonStatisticBebris.lesson_id,
            LessonStatisticBebris.user_id,
            func.round(func.avg(LessonStatisticBebris.accuracy)\
                .over(
                    partition_by=[LessonStatisticBebris.lesson_id, LessonStatisticBebris.user_id],
                    order_by=LessonStatisticBebris.created_at.desc(),
                    rows=(0, 2)
                )).label('avg_accuracy'),
            func.row_number()\
            .over(
                partition_by=LessonStatisticBebris.lesson_id,
                order_by=LessonStatisticBebris.created_at.desc()
            ).label('rn')
        ).where(LessonStatisticBebris.user_id == user_id)\
        .cte('ranked_stats')

        query = (
            select(
                LessonBebris.id,
                LessonBebris.lesson_title,
                subquery.c.avg_accuracy,
                LessonBebris.lesson_number
            )
            .outerjoin(subquery, LessonBebris.id == subquery.c.lesson_id)
            .where(((subquery.c.rn == 1) |  (subquery.c.lesson_id == None)) & (LessonBebris.playlist_id == playlist_id))
        )
        return (await self.session.execute(query)).all()

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
        data = {
            'user_id': user_id,
            'lesson_id': lesson_id,
            'correct_answers': correct_answers,
            'wrong_answers': wrong_answers,
            'accuracy': accuracy,
        }
        await self.session.merge(LessonStatisticBebris(**data))

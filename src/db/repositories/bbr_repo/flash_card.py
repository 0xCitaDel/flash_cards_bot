from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bbr_models import FlashCardBebris
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


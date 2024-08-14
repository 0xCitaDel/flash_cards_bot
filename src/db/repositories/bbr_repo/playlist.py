from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.bbr_models import PlaylistBebris
from db.repositories.abstract import AbstractRepository


class PlaylistBebrisRepo(AbstractRepository[PlaylistBebris]):
    """Lesosn repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=PlaylistBebris, session=session)


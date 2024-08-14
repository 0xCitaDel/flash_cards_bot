from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.structures.role import Role

from ..models import Base, User
from .abstract import AbstractRepository


class UserRepo(AbstractRepository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def get_by_user_id(self, user_id):

        query = select(self.type_model).where(User.user_id==user_id)
        res = (await self.session.execute(query)).first()
        return res

    async def new(
            self,
            user_id: int,
            user_name: Optional[str]=None,
            first_name: Optional[str]=None,
            second_name: Optional[str]=None,
            is_premium: bool=False,
            is_banned: bool=False,
            role: Role=Role.USER
    ) -> None:
        """Insert a new user into the database.

        :param user_id: Telegram user id
        :param user_name: Telegram username
        :param first_name: Telegram profile first name
        :param second_name: Telegram profile second name
        :param is_premium: Telegram user premium status
        :param is_banned: Checks if the user is banned
        :param role: User's role
        """
        await self.session.merge(
            User(
                user_id=user_id,
                user_name=user_name,
                first_name=first_name,
                second_name=second_name,
                is_premium=is_premium,
                is_banned=is_banned,
                role=role
            )
        )

    async def get_role(self, user_id: int) -> Role:
        """Get user role by id."""
        return await self.session.scalar(
            select(User.role).where(User.user_id == user_id).limit(1)
        )

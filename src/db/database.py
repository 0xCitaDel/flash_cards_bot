from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from config import settings as conf
from db.repositories.bbr_repo.flash_card import FlashCardBebrisRepo, FlashCardStatisticBebrisRepo

from .repositories import UserRepo
from .repositories.bbr_repo.playlist import PlaylistBebrisRepo
from .repositories.bbr_repo.lesson import LessonBebrisRepo, LessonStatisticBebrisRepo


def create_async_engine(url: URL | str) -> AsyncEngine:
    """Create async engine with given URL.

    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=conf.db.debug, pool_pre_ping=True)


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions.
    """

    user: UserRepo
    bbr_playlist: PlaylistBebrisRepo
    bbr_lesson: LessonBebrisRepo
    bbr_flash_card: FlashCardBebrisRepo
    bbr_lesson_statistic: LessonStatisticBebrisRepo
    bbr_flash_card_statistic: FlashCardStatisticBebrisRepo
    """ User repository """

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo = None,
        bbr_playlist: PlaylistBebrisRepo = None,
        bbr_lesson: LessonBebrisRepo = None,
        bbr_flash_card: FlashCardBebrisRepo = None,
        bbr_lesson_statistic: LessonStatisticBebrisRepo = None,
        bbr_flash_card_statistic: FlashCardStatisticBebrisRepo = None
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        :param user: (Optional) User repository
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.bbr_playlist = bbr_playlist or PlaylistBebrisRepo(session=session)
        self.bbr_lesson = bbr_lesson or LessonBebrisRepo(session=session)
        self.bbr_flash_card = bbr_flash_card or FlashCardBebrisRepo(session=session)
        self.bbr_lesson_statistic = bbr_lesson_statistic or LessonStatisticBebrisRepo(session=session)
        self.bbr_flash_card_statistic = bbr_flash_card_statistic or FlashCardStatisticBebrisRepo(session=session)

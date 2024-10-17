import datetime
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class LessonBebris(Base):
    __tablename__ = 'bebris_lessons'

    playlist_id: Mapped[int] = mapped_column(
        sa.ForeignKey('bebris_playlists.id'), unique=False, nullable=False
    )
    lesson_title: Mapped[str] = mapped_column(
        sa.String, unique=False, nullable=False
    )
    lesson_nubmer: Mapped[str] = mapped_column(
        sa.String, unique=False, nullable=False
    )
    video_nubmer: Mapped[str] = mapped_column(
        sa.String, unique=False, nullable=False
    )
    def __repr__(self) -> str:
        return f"LessonBebris(id={self.id!r}, playlist_id={self.playlist_id!r}, lesson_title={self.lesson_title!r})"


class LessonStatisticBebris(Base):
    __tablename__ = 'bebris_lesson_statistics'

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey('users.id'), unique=False, nullable=False
    )
    lesson_id: Mapped[int] = mapped_column(
        sa.ForeignKey('bebris_lessons.id'), unique=False, nullable=False
    )
    correct_answers: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=False
    )
    wrong_answers: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=False
    )
    accuracy: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=sa.text("TIMEZONE('utc', now())")
    )

    def __repr__(self) -> str:
        return f"LessonStatisticBebris(id={self.id!r}, user_id={self.user_id!r}, lesson_id={self.lesson_id!r})"

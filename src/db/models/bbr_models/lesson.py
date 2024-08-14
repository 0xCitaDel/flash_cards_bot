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
        sa.String, unique=True, nullable=False
    )
    lesson_nubmer: Mapped[list[int]] = mapped_column(
        sa.String, unique=False, nullable=False
    )
    video_nubmer: Mapped[list[int]] = mapped_column(
        sa.String, unique=False, nullable=False
    )


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

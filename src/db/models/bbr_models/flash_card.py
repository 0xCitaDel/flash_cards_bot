import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class FlashCardBebris(Base):
    __tablename__ = 'bebris_flash_cards'

    lesson_id: Mapped[int] = mapped_column(
        sa.ForeignKey('bebris_lessons.id'), unique=False, nullable=False
    )
    front_side: Mapped[str] = mapped_column(
        sa.String, unique=False, nullable=False
    )
    back_side: Mapped[str] = mapped_column(
        sa.String, unique=False, nullable=False
    )

    def __repr__(self) -> str:
        return f"FlashCardBebris(id={self.id!r}, back_side={self.back_side!r})"


class FlashCardStatisticBebris(Base):
    __tablename__ = 'bebris_flash_cards_statistics'

    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey('users.id'), unique=False, nullable=False
    )
    playlist_id: Mapped[int] = mapped_column(
        sa.ForeignKey('bebris_flash_cards.id'), unique=False, nullable=False
    )
    lesson_id: Mapped[int] = mapped_column(
        sa.ForeignKey('bebris_flash_cards.id'), unique=False, nullable=False
    )
    flashcard_id: Mapped[int] = mapped_column(
        sa.ForeignKey('bebris_flash_cards.id'), unique=False, nullable=False
    )
    correct_count: Mapped[int] = mapped_column(
        sa.Integer, unique=False, nullable=False, default=0
    )
    last_result: Mapped[bool] = mapped_column(
        sa.Boolean, unique=False, nullable=False
    )

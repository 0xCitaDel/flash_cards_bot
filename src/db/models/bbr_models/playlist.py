import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class PlaylistBebris(Base):
    __tablename__ = 'bebris_playlists'

    playlist_name: Mapped[str] = mapped_column(
        sa.String, unique=True, nullable=False
    )
    playlist_color: Mapped[str] = mapped_column(
        sa.String, unique=True, nullable=False
    )
    emoji: Mapped[str] = mapped_column(
        sa.String, unique=False, nullable=True
    )

    def __repr__(self) -> str:
        return f"PlaylistBebris(id={self.id!r}, playlist_name={self.playlist_name!r})"

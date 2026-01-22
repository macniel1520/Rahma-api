from __future__ import annotations

import datetime as dt
import uuid

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK


class RefreshToken(Base, TimestampMixin):
    __tablename__ = "refresh_token"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)

    userId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    tokenHash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    expiresAt: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revokedAt: Mapped[dt.datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

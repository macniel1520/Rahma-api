import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK

if TYPE_CHECKING:
    from app.db.models.user import User


class PasswordResetCode(Base, TimestampMixin):
    __tablename__ = "password_reset_code"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    expiresAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    userId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="password_reset_codes")

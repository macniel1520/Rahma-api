import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, DateTime
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
    from app.db.models.user import User


class EmailVerification(Base, TimestampMixin):
    __tablename__ = "email_verification"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(255), nullable=False)
    expiresAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    userId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="email_verifications")

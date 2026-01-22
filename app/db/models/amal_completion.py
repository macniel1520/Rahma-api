import uuid
import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Date, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK

if TYPE_CHECKING:
    from app.db.models.amal import Amal
    from app.db.models.user import User


class AmalCompletion(Base, TimestampMixin):
    __tablename__ = "amal_completion"
    __table_args__ = (
        UniqueConstraint("amalId", "date", name="uq_amal_completion_amal_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    amalId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("amal.id", ondelete="CASCADE"), nullable=False
    )
    userId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    completedAt: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    amal: Mapped["Amal"] = relationship("Amal", back_populates="completions")
    user: Mapped["User"] = relationship("User", back_populates="amal_completions")

import uuid
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, Time, String, Enum
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK, ReccuringRule
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.amal_category import AmalCategory
    from app.db.models.icon import Icon



class Amal(Base, TimestampMixin):
    __tablename__ = "amal"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    reccuringRule: Mapped[ReccuringRule] = mapped_column(
        Enum(ReccuringRule, name="reccuring_rule_enum"), nullable=False
    )

    amalCategoryId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("amal_category.id", ondelete="SET NULL"), nullable=True
    )
    userId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    iconId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("icon.id", ondelete="SET NULL"), nullable=True
    )

    icon: Mapped["Icon"] = relationship("Icon", back_populates="amals")
    user: Mapped["User"] = relationship("User", back_populates="amals")
    amal_category: Mapped["AmalCategory"] = relationship("AmalCategory", back_populates="amals")

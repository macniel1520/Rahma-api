import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Text, ForeignKey
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK, Role
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user import User


class Message(Base, TimestampMixin):
    __tablename__ = "message"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, name="role_enum"), nullable=False)

    userId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="messages")

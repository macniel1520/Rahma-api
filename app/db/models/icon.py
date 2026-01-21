import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK

if TYPE_CHECKING:
    from app.db.models.amal import Amal


class Icon(Base, TimestampMixin):
    __tablename__ = "icon"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    url: Mapped[str] = mapped_column(String(500), nullable=False)

    # Back-references
    amals: Mapped[list["Amal"]] = relationship("Amal", back_populates="icon")

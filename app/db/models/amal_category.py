import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK

if TYPE_CHECKING:
    from app.db.models.amal import Amal


class AmalCategory(Base, TimestampMixin):
    __tablename__ = "amal_category"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    amals: Mapped[list["Amal"]] = relationship("Amal", back_populates="amal_category")

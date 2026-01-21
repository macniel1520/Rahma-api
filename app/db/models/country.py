import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK

if TYPE_CHECKING:
    from app.db.models.route import Route


class Country(Base, TimestampMixin):
    __tablename__ = "country"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    photoUrl: Mapped[str] = mapped_column(String(500), nullable=False)

    routes: Mapped[list["Route"]] = relationship("Route", back_populates="country")

    routes: Mapped[list["Route"]] = relationship("Route", back_populates="country")

import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Float, BIGINT
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.location import Location
    from app.db.models.route import Route


class Hotel(Base, TimestampMixin):
    __tablename__ = "hotel"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    photoUrl: Mapped[str] = mapped_column(String(500), nullable=False)
    avgScore: Mapped[float] = mapped_column(Float, nullable=False)
    scoreCount: Mapped[BIGINT] = mapped_column(BIGINT, nullable=False)
    avgPrice: Mapped[float] = mapped_column(Float, nullable=False)

    routeId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("route.id", ondelete="CASCADE"), nullable=False
    )
    route: Mapped["Route"] = relationship("Route", back_populates="hotels")
    locationId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("location.id", ondelete="SET NULL"), nullable=True
    )
    location: Mapped["Location"] = relationship("Location", back_populates="hotels")

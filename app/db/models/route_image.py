import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import URL, ForeignKey
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.route import Route


class RouteImage(Base, TimestampMixin):
    __tablename__ = "route_image"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    url: Mapped[URL] = mapped_column(URL, nullable=False)

    routeId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("route.id", ondelete="CASCADE"), nullable=False
    )
    route: Mapped["Route"] = relationship("Route", back_populates="route_images")

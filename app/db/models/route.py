import uuid
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK, Category

if TYPE_CHECKING:
    from app.db.models.amal_template import AmalTemplate
    from app.db.models.country import Country
    from app.db.models.hotel import Hotel
    from app.db.models.restaurant import Restaurant
    from app.db.models.route_image import RouteImage


class Route(Base, TimestampMixin):
    __tablename__ = "route"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    views: Mapped[BIGINT] = mapped_column(BIGINT, nullable=False)
    photoUrl: Mapped[str] = mapped_column(String(500), nullable=False)

    category: Mapped[Category] = mapped_column(
        Enum(Category, name="category_enum"), nullable=False
    )

    countryId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("country.id", ondelete="CASCADE"), nullable=False
    )
    country: Mapped["Country"] = relationship("Country", back_populates="routes")

    route_images: Mapped[list["RouteImage"]] = relationship(
        "RouteImage", back_populates="route", cascade="all, delete-orphan"
    )
    restaurants: Mapped[list["Restaurant"]] = relationship(
        "Restaurant", back_populates="route", cascade="all, delete-orphan"
    )
    hotels: Mapped[list["Hotel"]] = relationship(
        "Hotel", back_populates="route", cascade="all, delete-orphan"
    )
    amal_templates: Mapped[list["AmalTemplate"]] = relationship(
        "AmalTemplate", back_populates="route", cascade="all, delete-orphan"
    )

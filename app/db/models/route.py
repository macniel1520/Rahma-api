import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Enum, BIGINT, URL
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK, Category
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.country import Country


class Route(Base, TimestampMixin):
    __tablename__ = "route"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    views: Mapped[BIGINT] = mapped_column(BIGINT, nullable=False)
    routeUrl: Mapped[URL] = mapped_column(URL, nullable=False)
    
    category: Mapped[Category] = mapped_column(
        Enum(Category, name="category_enum"), nullable=False
    )

    countryId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("country.id", ondelete="CASCADE"), nullable=False
    )
    country: Mapped["Country"] = relationship("Country", back_populates="routes")

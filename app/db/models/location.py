import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK


class Location(Base, TimestampMixin):
    __tablename__ = "location"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    lat: Mapped[str] = mapped_column(String(255), nullable=False)
    lng: Mapped[str] = mapped_column(String(255), nullable=False)

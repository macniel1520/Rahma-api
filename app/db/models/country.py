import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import URL, String
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK


class Country(Base, TimestampMixin):
    __tablename__ = "country"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    photoUrl: Mapped[URL] = mapped_column(URL, nullable=False)

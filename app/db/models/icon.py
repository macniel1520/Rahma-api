import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import URL
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK


class Icon(Base, TimestampMixin):
    __tablename__ = "icon"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    url: Mapped[URL] = mapped_column(URL, nullable=False)

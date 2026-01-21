import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK


class AmalCategory(Base, TimestampMixin):
    __tablename__ = "amal_category"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

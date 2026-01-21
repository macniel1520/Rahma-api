import uuid
import datetime
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import Mapped, mapped_column, synonym
from sqlalchemy import String, Boolean, Date

from app.core.config import settings
from app.db.models.enums import UUID_PK
from app.db.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    email: Mapped[EmailType] = mapped_column(EmailType, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    isVerified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    isActive: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    isSuperuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    dateOfBirth: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    gender: Mapped[str] = mapped_column(String(255), nullable=True)
    country: Mapped[str] = mapped_column(String(255), nullable=True)
    avatarUrl: Mapped[str] = mapped_column(
        String(500), default=settings.s3.url + "/avatars/default.png"
    )

    hashed_password = synonym("password")
    is_verified = synonym("isVerified")
    is_active = synonym("isActive")
    is_superuser = synonym("isSuperuser")

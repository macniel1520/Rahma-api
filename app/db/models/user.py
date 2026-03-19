import datetime
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym
from sqlalchemy_utils import EmailType

from app.core.config import settings
from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK

if TYPE_CHECKING:
    from app.db.models.message import Message
    from app.db.models.email_verification import EmailVerification
    from app.db.models.amal import Amal
    from app.db.models.amal_completion import AmalCompletion
    from app.db.models.password_reset_code import PasswordResetCode


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

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")
    email_verifications: Mapped[list["EmailVerification"]] = relationship(
        "EmailVerification", back_populates="user"
    )
    password_reset_codes: Mapped[list["PasswordResetCode"]] = relationship(
        "PasswordResetCode",
        back_populates="user",
    )
    amals: Mapped[list["Amal"]] = relationship("Amal", back_populates="user")
    amal_completions: Mapped[list["AmalCompletion"]] = relationship(
        "AmalCompletion", back_populates="user"
    )

    def __str__(self) -> str:
        return self.name or self.email

import datetime

from pydantic import EmailStr

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from pydantic import Field


class UserRead(AttributeMixin, UUIDMixin):
    email: EmailStr

    isVerified: bool

    name: str | None = None
    dateOfBirth: datetime.date | None = None
    gender: str | None = None
    country: str | None = None
    avatarUrl: str | None = None


class UserCreate(AttributeMixin):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    name: str | None = None
    dateOfBirth: datetime.date | None = None
    gender: str | None = None
    country: str | None = None


class UserUpdate(AttributeMixin):
    password: str | None = Field(default=None, min_length=8, max_length=128)

    name: str | None = None
    dateOfBirth: datetime.date | None = None
    gender: str | None = None
    country: str | None = None
    avatarUrl: str | None = None

import datetime

from pydantic import EmailStr

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin


class UserRead(AttributeMixin, UUIDMixin):
    email: EmailStr

    isVerified: bool

    name: str | None = None
    dateOfBirth: datetime.date | None = None
    gender: str | None = None
    country: str | None = None
    avatarUrl: str | None = None


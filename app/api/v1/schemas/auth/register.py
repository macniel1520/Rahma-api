from __future__ import annotations

import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    name: str | None = None
    dateOfBirth: datetime.date | None = None
    gender: str | None = None
    country: str | None = None
    avatarUrl: str | None = None

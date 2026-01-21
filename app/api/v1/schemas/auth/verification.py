from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RequestVerifyIn(BaseModel):
    email: EmailStr


class VerifyCodeIn(BaseModel):
    email: EmailStr
    code: str = Field(min_length=4, max_length=4)

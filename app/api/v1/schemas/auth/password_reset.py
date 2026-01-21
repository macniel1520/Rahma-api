from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class RequestResetCodeIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    email: EmailStr
    code: str = Field(min_length=4, max_length=4)
    new_password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)

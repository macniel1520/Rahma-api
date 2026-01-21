from __future__ import annotations

from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class TokenPairOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"


class RefreshIn(BaseModel):
    refresh_token: str = Field(min_length=20)


class LogoutIn(BaseModel):
    refresh_token: str = Field(min_length=20)

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
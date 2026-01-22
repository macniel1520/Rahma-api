# app/services/auth/user_manager.py

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.engine import get_session
from app.db.models.user import User
from app.utils.emailer import send_email


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.user_token.secret
    verification_token_secret = settings.user_token.secret

    async def authenticate(self, credentials):
        user = await super().authenticate(credentials)
        if user and not user.is_verified:
            raise exceptions.user_not_verified_exc()
        return user

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        await send_email(
            to=str(user.email),
            subject="Email verification",
            body=(
                "Use this verification token in the app:\n\n"
                f"{token}\n\n"
                "If you didn't request this, ignore this message."
            ),
        )

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        await send_email(
            to=str(user.email),
            subject="Password reset",
            body=(
                "Use this password reset token in the app:\n\n"
                f"{token}\n\n"
                "If you didn't request this, ignore this message."
            ),
        )


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

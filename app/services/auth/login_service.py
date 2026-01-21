from __future__ import annotations

from uuid import UUID

from fastapi_users.manager import BaseUserManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.services.auth.access_issuer import issue_access_token
from app.services.auth.refresh_service import issue_refresh
from app.utils.types import TokenPair

class InvalidCredentials(Exception):
    pass


async def login_with_email_password(
    *,
    session: AsyncSession,
    user_manager: BaseUserManager[User, UUID],
    email: str,
    password: str,
) -> TokenPair:
    class _Creds:
        username: str
        password: str

        def __init__(self, username: str, password: str):
            self.username = username
            self.password = password

    user = await user_manager.authenticate(_Creds(username=email, password=password))
    if not user:
        raise InvalidCredentials()

    access = await issue_access_token(user)

    refresh = await issue_refresh(session, user_id=user.id)

    return TokenPair(access_token=access, refresh_token=refresh)

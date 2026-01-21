from __future__ import annotations

import datetime
import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.cruds.email_verifications import (
    delete_by_user_id as delete_email_verifications,
    get_latest_by_user_and_code as get_email_verification,
    save_code as save_email_verification_code,
)
from app.db.cruds.password_reset_codes import (
    delete_by_user_id as delete_password_reset_codes,
    get_latest_by_user_and_code as get_password_reset_code,
    save_code as save_password_reset_code,
)
from app.db.cruds.users import create as create_user_record, get_by_email
from app.db.models.user import User
from app.services.auth.passwords import hash_password, verify_password
from app.services.auth.tokens import issue_access_token, issue_refresh
from app.utils.types import TokenPair
from app.utils.emailer import send_email


class EmailTaken(Exception):
    pass


class InvalidCode(Exception):
    pass


class CodeExpired(Exception):
    pass


class PasswordMismatch(Exception):
    pass


class InvalidCredentials(Exception):
    pass


def _verification_expires_at() -> datetime.datetime:
    return datetime.datetime.utcnow() + datetime.timedelta(
        seconds=int(settings.user_token.lifetime_seconds)
    )


def _reset_expires_at() -> datetime.datetime:
    return datetime.datetime.utcnow() + datetime.timedelta(
        seconds=int(settings.user_token.lifetime_seconds)
    )


def _generate_code() -> str:
    # 4-digit code
    return f"{secrets.randbelow(10000):04d}"


async def register_user(
    *,
    session: AsyncSession,
    email: str,
    password: str,
    name: str | None = None,
    date_of_birth: datetime.date | None = None,
    gender: str | None = None,
    country: str | None = None,
    avatar_url: str | None = None,
) -> User:
    existing = await get_by_email(session, email)
    if existing:
        raise EmailTaken()

    user = User(
        email=email,
        password=hash_password(password),
        isVerified=False,
        isActive=True,
        isSuperuser=False,
        name=name,
        dateOfBirth=date_of_birth,
        gender=gender,
        country=country,
    )
    if avatar_url is not None:
        user.avatarUrl = avatar_url

    await create_user_record(session, user)
    await session.commit()
    await session.refresh(user)

    code = _generate_code()
    await save_email_verification_code(
        session,
        user_id=user.id,
        code=code,
        expires_at=_verification_expires_at(),
    )
    await session.commit()

    await send_email(
        to=str(user.email),
        subject="Email verification",
        body=(
            "Use this verification code in the app:\n\n"
            f"{code}\n\n"
            "If you didn't request this, ignore this message."
        ),
    )
    return user


async def request_verify_code(
    *,
    session: AsyncSession,
    email: str,
) -> None:
    user = await get_by_email(session, email)
    if not user or user.is_verified:
        return None

    code = _generate_code()
    await save_email_verification_code(
        session,
        user_id=user.id,
        code=code,
        expires_at=_verification_expires_at(),
    )
    await session.commit()

    await send_email(
        to=str(user.email),
        subject="Email verification",
        body=(
            "Use this verification code in the app:\n\n"
            f"{code}\n\n"
            "If you didn't request this, ignore this message."
        ),
    )
    return None


async def verify_code(
    *,
    session: AsyncSession,
    email: str,
    code: str,
) -> User:
    user = await get_by_email(session, email)
    if not user:
        raise InvalidCode()

    if user.is_verified:
        return user

    verification = await get_email_verification(
        session,
        user_id=user.id,
        code=code,
    )
    if not verification:
        raise InvalidCode()

    if verification.expiresAt < datetime.datetime.utcnow():
        await delete_email_verifications(session, user_id=user.id)
        await session.commit()
        raise CodeExpired()

    user.is_verified = True
    await session.commit()
    await delete_email_verifications(session, user_id=user.id)
    await session.commit()
    return user


async def request_reset_code(
    *,
    session: AsyncSession,
    email: str,
) -> None:
    user = await get_by_email(session, email)
    if not user:
        return None

    code = _generate_code()
    await save_password_reset_code(
        session,
        user_id=user.id,
        code=code,
        expires_at=_reset_expires_at(),
    )
    await session.commit()

    await send_email(
        to=str(user.email),
        subject="Password reset",
        body=(
            "Use this password reset code in the app:\n\n"
            f"{code}\n\n"
            "If you didn't request this, ignore this message."
        ),
    )
    return None


async def reset_password(
    *,
    session: AsyncSession,
    email: str,
    code: str,
    new_password: str,
    confirm_password: str,
) -> None:
    user = await get_by_email(session, email)
    if not user:
        raise InvalidCode()

    if new_password != confirm_password:
        raise PasswordMismatch()

    reset_code = await get_password_reset_code(
        session,
        user_id=user.id,
        code=code,
    )
    if not reset_code:
        raise InvalidCode()

    if reset_code.expiresAt < datetime.datetime.utcnow():
        await delete_password_reset_codes(session, user_id=user.id)
        await session.commit()
        raise CodeExpired()

    user.password = hash_password(new_password)
    await session.commit()
    await delete_password_reset_codes(session, user_id=user.id)
    await session.commit()
    return None


async def login_with_email_password(
    *,
    session: AsyncSession,
    email: str,
    password: str,
) -> TokenPair:
    user = await get_by_email(session, email)
    if not user:
        raise InvalidCredentials()

    if not user.is_active or not user.is_verified:
        raise InvalidCredentials()

    if not verify_password(password, user.password):
        raise InvalidCredentials()

    access = issue_access_token(user)
    refresh = await issue_refresh(session, user_id=user.id)

    return TokenPair(access_token=access, refresh_token=refresh)

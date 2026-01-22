from __future__ import annotations

import datetime as dt
import uuid
from typing import Any
from uuid import UUID

import jwt

from app.core.config import settings
from app.db.cruds.refresh_tokens import get_by_token_hash, create, revoke_by_token_hash
from app.db.models.refresh import RefreshToken
from app.db.models.user import User
from app.utils.time import now_utc
from app.utils.types import TokenPair


class AccessTokenError(Exception):
    pass


class RefreshTokenError(Exception):
    pass


class InvalidRefresh(Exception):
    pass


def _access_expires_at() -> dt.datetime:
    return now_utc() + dt.timedelta(seconds=int(settings.jwt.lifetime_seconds))


def _refresh_expires_at() -> dt.datetime:
    return now_utc() + dt.timedelta(
        seconds=int(settings.refresh_token.lifetime_seconds)
    )


def encode_access_token(*, user_id: UUID) -> str:
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "typ": "access",
        "iat": now_utc(),
        "exp": _access_expires_at(),
    }
    return jwt.encode(payload, settings.jwt.secret, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.jwt.secret, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise AccessTokenError("invalid_token") from exc

    if payload.get("typ") != "access":
        raise AccessTokenError("invalid_token_type")

    return payload


def encode_refresh_token(*, user_id: UUID, jti: str) -> str:
    """
    Создаёт JWT refresh токен.
    jti - уникальный идентификатор токена, хранится в БД для отзыва.
    """
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "typ": "refresh",
        "jti": jti,
        "iat": now_utc(),
        "exp": _refresh_expires_at(),
    }
    return jwt.encode(payload, settings.jwt.secret, algorithm="HS256")


def decode_refresh_token(token: str) -> dict[str, Any]:
    """
    Декодирует и валидирует JWT refresh токен.
    Возвращает payload с claims: sub, typ, jti, iat, exp.
    """
    try:
        payload = jwt.decode(token, settings.jwt.secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise RefreshTokenError("token_expired") from exc
    except jwt.PyJWTError as exc:
        raise RefreshTokenError("invalid_token") from exc

    if payload.get("typ") != "refresh":
        raise RefreshTokenError("invalid_token_type")

    if not payload.get("jti"):
        raise RefreshTokenError("missing_jti")

    return payload


def issue_access_token(user: User) -> str:
    return encode_access_token(user_id=user.id)


async def issue_refresh(session, *, user_id: UUID) -> str:
    """
    Выпускает JWT refresh токен и сохраняет jti в БД.
    Возвращает JWT refresh токен (его отдаём клиенту).
    """
    jti = str(uuid.uuid4())
    expires_at = _refresh_expires_at()

    rt = RefreshToken(
        userId=user_id,
        tokenHash=jti,  # используем jti как уникальный идентификатор
        expiresAt=expires_at,
        revokedAt=None,
    )

    await create(session, rt)
    await session.commit()

    return encode_refresh_token(user_id=user_id, jti=jti)


async def rotate_refresh(session, *, refresh_token: str) -> TokenPair:
    """
    Ротация refresh токена: отзывает старый и выдаёт новую пару токенов.
    """
    try:
        payload = decode_refresh_token(refresh_token)
    except RefreshTokenError:
        raise InvalidRefresh()

    jti = payload["jti"]
    user_id = UUID(payload["sub"])

    rt = await get_by_token_hash(session, jti)
    if not rt:
        raise InvalidRefresh()

    if rt.revokedAt is not None:
        raise InvalidRefresh()

    # Отзываем текущий токен
    rt.revokedAt = now_utc()
    await session.flush()

    # Создаём новый токен
    new_jti = str(uuid.uuid4())
    new_expires_at = _refresh_expires_at()

    new_rt = RefreshToken(
        userId=user_id,
        tokenHash=new_jti,
        expiresAt=new_expires_at,
        revokedAt=None,
    )
    await create(session, new_rt)

    user = await session.get(User, user_id)
    if not user or not user.is_active or not user.is_verified:
        raise InvalidRefresh()

    access = issue_access_token(user)
    new_refresh = encode_refresh_token(user_id=user_id, jti=new_jti)

    await session.commit()

    return TokenPair(access_token=access, refresh_token=new_refresh)


async def revoke_refresh(session, *, refresh_token: str) -> None:
    """
    Отзывает refresh токен по его JWT.
    """
    try:
        payload = decode_refresh_token(refresh_token)
    except RefreshTokenError:
        # Токен уже невалиден, ничего не делаем
        return

    jti = payload["jti"]
    await revoke_by_token_hash(session, jti, revoked_at=now_utc())
    await session.commit()

from __future__ import annotations

import datetime as dt
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.refresh import RefreshToken
from app.db.models.user import User
from app.db.cruds.refresh_repository import get_by_token_hash, create, revoke_by_token_hash
from app.services.auth.access_issuer import issue_access_token
from app.utils.crypto import make_opaque_token, sha256_hex
from app.utils.time import now_utc
from app.utils.types import TokenPair

class InvalidRefresh(Exception):
    pass

def _refresh_expires_at() -> dt.datetime:
    return now_utc() + dt.timedelta(seconds=int(settings.refresh_token.lifetime_seconds))


def _refresh_bytes() -> int:
    return int(settings.refresh_token.bytes_length)


async def issue_refresh(session: AsyncSession, *, user_id: UUID) -> str:
    """
    Выпускает refresh (opaque) и сохраняет hash в БД.
    Возвращает plaintext refresh токен (его отдаём клиенту).
    """
    plain = make_opaque_token(_refresh_bytes())
    token_hash = sha256_hex(plain)

    rt = RefreshToken(
        userId=user_id,
        tokenHash=token_hash,
        expiresAt=_refresh_expires_at(),
        revokedAt=None,
    )

    await create(session, rt)
    await session.commit()
    return plain


async def rotate_refresh(session: AsyncSession, *, refresh_token: str) -> TokenPair:
    token_hash = sha256_hex(refresh_token)

    rt = await get_by_token_hash(session, token_hash)
    if not rt:
        raise InvalidRefresh()

    if rt.revokedAt is not None or rt.expiresAt <= now_utc():
        raise InvalidRefresh()

    rt.revokedAt = now_utc()
    await session.flush()

    new_plain = make_opaque_token(_refresh_bytes())
    new_hash = sha256_hex(new_plain)

    new_rt = RefreshToken(
        userId=rt.userId,
        tokenHash=new_hash,
        expiresAt=_refresh_expires_at(),
        revokedAt=None,
    )
    await create(session, new_rt)

    user = await session.get(User, rt.userId)
    if not user or not user.is_active:
        raise InvalidRefresh()

    access = await issue_access_token(user)

    await session.commit()

    return TokenPair(access_token=access, refresh_token=new_plain)


async def revoke_refresh(session: AsyncSession, *, refresh_token: str) -> None:
    token_hash = sha256_hex(refresh_token)
    await revoke_by_token_hash(session, token_hash, revoked_at=now_utc())
    await session.commit()

from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.refresh import RefreshToken


async def get_by_token_hash(session: AsyncSession, token_hash: str) -> RefreshToken | None:
    res = await session.execute(
        select(RefreshToken).where(RefreshToken.tokenHash == token_hash)
    )
    return res.scalar_one_or_none()


async def create(session: AsyncSession, rt: RefreshToken) -> RefreshToken:
    session.add(rt)
    await session.flush()
    return rt


async def revoke_by_token_hash(session: AsyncSession, token_hash: str, revoked_at) -> None:
    await session.execute(
        update(RefreshToken)
        .where(RefreshToken.tokenHash == token_hash, RefreshToken.revokedAt.is_(None))
        .values(revokedAt=revoked_at)
    )

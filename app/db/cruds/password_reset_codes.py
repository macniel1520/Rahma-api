from __future__ import annotations

import datetime
import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.password_reset_code import PasswordResetCode


async def save_code(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    code: str,
    expires_at: datetime.datetime,
) -> PasswordResetCode:
    await session.execute(
        delete(PasswordResetCode).where(PasswordResetCode.userId == user_id)
    )
    reset_code = PasswordResetCode(
        userId=user_id,
        code=code,
        expiresAt=expires_at,
    )
    session.add(reset_code)
    await session.flush()
    return reset_code


async def get_latest_by_user_and_code(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    code: str,
) -> PasswordResetCode | None:
    res = await session.execute(
        select(PasswordResetCode)
        .where(
            PasswordResetCode.userId == user_id,
            PasswordResetCode.code == code,
        )
        .order_by(PasswordResetCode.createdAt.desc())
    )
    return res.scalars().first()


async def delete_by_user_id(session: AsyncSession, *, user_id: uuid.UUID) -> None:
    await session.execute(
        delete(PasswordResetCode).where(PasswordResetCode.userId == user_id)
    )

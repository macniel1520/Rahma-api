from __future__ import annotations

import datetime
import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.email_verification import EmailVerification


async def save_code(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    code: str,
    expires_at: datetime.datetime,
) -> EmailVerification:
    await session.execute(
        delete(EmailVerification).where(EmailVerification.userId == user_id)
    )
    verification = EmailVerification(
        userId=user_id,
        code=code,
        expiresAt=expires_at,
    )
    session.add(verification)
    await session.flush()
    return verification


async def get_latest_by_user_and_code(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    code: str,
) -> EmailVerification | None:
    res = await session.execute(
        select(EmailVerification)
        .where(
            EmailVerification.userId == user_id,
            EmailVerification.code == code,
        )
        .order_by(EmailVerification.createdAt.desc())
    )
    return res.scalars().first()


async def delete_by_user_id(session: AsyncSession, *, user_id: uuid.UUID) -> None:
    await session.execute(
        delete(EmailVerification).where(EmailVerification.userId == user_id)
    )

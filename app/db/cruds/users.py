from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


async def get_by_email(session: AsyncSession, email: str) -> User | None:
    res = await session.execute(
        select(User).where(func.lower(User.email) == func.lower(email))
    )
    return res.scalar_one_or_none()


async def get_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    return await session.get(User, user_id)


async def create(session: AsyncSession, user: User) -> User:
    session.add(user)
    await session.flush()
    return user

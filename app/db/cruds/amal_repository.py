from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.amal import Amal


@runtime_checkable
class AmalRepository(Protocol):
    async def get_all_by_user(self, *, user_id: UUID) -> Sequence[Amal]: ...
    async def get_by_id(self, *, amal_id: UUID) -> Amal | None: ...
    async def get_by_ids(self, *, amal_ids: list[UUID]) -> Sequence[Amal]: ...
    async def upsert_many(self, *, amals: list[dict]) -> Sequence[Amal]: ...
    async def delete_by_ids(self, *, user_id: UUID, amal_ids: list[UUID]) -> int: ...


class SqlAlchemyAmalRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_by_user(self, *, user_id: UUID) -> list[Amal]:
        stmt = (
            select(Amal)
            .where(Amal.userId == user_id)
            .options(
                joinedload(Amal.icon),
                joinedload(Amal.category),
            )
            .order_by(Amal.createdAt.desc())
        )
        result = await self._session.scalars(stmt)
        return list(result.unique().all())

    async def get_by_id(self, *, amal_id: UUID) -> Amal | None:
        stmt = (
            select(Amal)
            .where(Amal.id == amal_id)
            .options(
                joinedload(Amal.icon),
                joinedload(Amal.category),
            )
        )
        result = await self._session.scalar(stmt)
        return result

    async def get_by_ids(self, *, amal_ids: list[UUID]) -> list[Amal]:
        if not amal_ids:
            return []
        stmt = (
            select(Amal)
            .where(Amal.id.in_(amal_ids))
            .options(
                joinedload(Amal.icon),
                joinedload(Amal.category),
            )
        )
        result = await self._session.scalars(stmt)
        return list(result.unique().all())

    async def upsert_many(self, *, amals: list[dict]) -> list[Amal]:
        if not amals:
            return []

        stmt = insert(Amal).values(amals)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Amal.id],
            set_={
                "title": stmt.excluded.title,
                "date": stmt.excluded.date,
                "time": stmt.excluded.time,
                "reccuringRule": stmt.excluded.reccuringRule,
                "amalCategoryId": stmt.excluded.amalCategoryId,
                "iconId": stmt.excluded.iconId,
            },
        )
        await self._session.execute(stmt)
        await self._session.flush()

        amal_ids = [amal["id"] for amal in amals]
        return await self.get_by_ids(amal_ids=amal_ids)

    async def delete_by_ids(self, *, user_id: UUID, amal_ids: list[UUID]) -> int:
        """Delete specific amals by IDs (only if they belong to user)."""
        if not amal_ids:
            return 0
        stmt = delete(Amal).where(
            Amal.userId == user_id,
            Amal.id.in_(amal_ids),
        )
        result = await self._session.execute(stmt)
        return result.rowcount

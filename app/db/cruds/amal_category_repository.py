from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.amal_category import AmalCategory


@runtime_checkable
class AmalCategoryRepository(Protocol):
    async def get_all(self) -> Sequence[AmalCategory]: ...
    async def get_by_id(self, *, category_id: UUID) -> AmalCategory | None: ...
    async def get_by_ids(
        self, *, category_ids: list[UUID]
    ) -> Sequence[AmalCategory]: ...
    async def upsert_many(
        self, *, categories: list[dict]
    ) -> Sequence[AmalCategory]: ...


class SqlAlchemyAmalCategoryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[AmalCategory]:
        stmt = select(AmalCategory).order_by(AmalCategory.createdAt.desc())
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, *, category_id: UUID) -> AmalCategory | None:
        stmt = select(AmalCategory).where(AmalCategory.id == category_id)
        result = await self._session.scalar(stmt)
        return result

    async def get_by_ids(self, *, category_ids: list[UUID]) -> list[AmalCategory]:
        if not category_ids:
            return []
        stmt = select(AmalCategory).where(AmalCategory.id.in_(category_ids))
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def upsert_many(self, *, categories: list[dict]) -> list[AmalCategory]:
        if not categories:
            return []

        stmt = insert(AmalCategory).values(categories)
        stmt = stmt.on_conflict_do_update(
            index_elements=[AmalCategory.id],
            set_={
                "name": stmt.excluded.name,
            },
        )
        await self._session.execute(stmt)
        await self._session.flush()

        category_ids = [cat["id"] for cat in categories]
        return await self.get_by_ids(category_ids=category_ids)

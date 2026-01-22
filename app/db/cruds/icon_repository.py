from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.icon import Icon


@runtime_checkable
class IconRepository(Protocol):
    async def get_all(self) -> Sequence[Icon]: ...
    async def get_by_id(self, *, icon_id: UUID) -> Icon | None: ...
    async def get_by_ids(self, *, icon_ids: list[UUID]) -> Sequence[Icon]: ...
    async def upsert_many(self, *, icons: list[dict]) -> Sequence[Icon]: ...


class SqlAlchemyIconRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Icon]:
        stmt = select(Icon).order_by(Icon.createdAt.desc())
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, *, icon_id: UUID) -> Icon | None:
        stmt = select(Icon).where(Icon.id == icon_id)
        result = await self._session.scalar(stmt)
        return result

    async def get_by_ids(self, *, icon_ids: list[UUID]) -> list[Icon]:
        if not icon_ids:
            return []
        stmt = select(Icon).where(Icon.id.in_(icon_ids))
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def upsert_many(self, *, icons: list[dict]) -> list[Icon]:
        if not icons:
            return []

        stmt = insert(Icon).values(icons)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Icon.id],
            set_={
                "url": stmt.excluded.url,
            },
        )
        await self._session.execute(stmt)
        await self._session.flush()

        icon_ids = [icon["id"] for icon in icons]
        return await self.get_by_ids(icon_ids=icon_ids)

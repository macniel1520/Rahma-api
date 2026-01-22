from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.restaurant import Restaurant


@runtime_checkable
class RestaurantRepository(Protocol):
    async def get_list_by_route(
        self,
        *,
        route_id: UUID,
        limit: int,
        offset: int,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> Sequence[Restaurant]: ...

    async def get_total_count(
        self,
        *,
        route_id: UUID,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> int: ...


class SqlAlchemyRestaurantRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_list_by_route(
        self,
        *,
        route_id: UUID,
        limit: int,
        offset: int,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> list[Restaurant]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        stmt = select(Restaurant).where(Restaurant.routeId == route_id)

        if min_score is not None:
            stmt = stmt.where(Restaurant.avgScore >= min_score)
        if max_score is not None:
            stmt = stmt.where(Restaurant.avgScore <= max_score)

        stmt = stmt.order_by(Restaurant.createdAt.desc()).offset(offset).limit(limit)

        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_total_count(
        self,
        *,
        route_id: UUID,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> int:
        stmt = select(func.count(Restaurant.id)).where(Restaurant.routeId == route_id)

        if min_score is not None:
            stmt = stmt.where(Restaurant.avgScore >= min_score)
        if max_score is not None:
            stmt = stmt.where(Restaurant.avgScore <= max_score)

        result = await self._session.scalar(stmt)
        return result or 0

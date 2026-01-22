from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.hotel import Hotel


@runtime_checkable
class HotelRepository(Protocol):
    async def get_list_by_route(
        self,
        *,
        route_id: UUID,
        limit: int,
        offset: int,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> Sequence[Hotel]: ...

    async def get_total_count(
        self,
        *,
        route_id: UUID,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> int: ...


class SqlAlchemyHotelRepository:
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
    ) -> list[Hotel]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        stmt = (
            select(Hotel)
            .where(Hotel.routeId == route_id)
            .options(joinedload(Hotel.location))
        )

        if min_score is not None:
            stmt = stmt.where(Hotel.avgScore >= min_score)
        if max_score is not None:
            stmt = stmt.where(Hotel.avgScore <= max_score)

        stmt = stmt.order_by(Hotel.createdAt.desc()).offset(offset).limit(limit)

        result = await self._session.scalars(stmt)
        return list(result.unique().all())

    async def get_total_count(
        self,
        *,
        route_id: UUID,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> int:
        stmt = select(func.count(Hotel.id)).where(Hotel.routeId == route_id)

        if min_score is not None:
            stmt = stmt.where(Hotel.avgScore >= min_score)
        if max_score is not None:
            stmt = stmt.where(Hotel.avgScore <= max_score)

        result = await self._session.scalar(stmt)
        return result or 0

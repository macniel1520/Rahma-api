from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.enums import Category
from app.db.models.hotel import Hotel
from app.db.models.restaurant import Restaurant
from app.db.models.route import Route


@runtime_checkable
class RouteRepository(Protocol):
    async def get_list(self, *, limit: int, offset: int) -> Sequence[Route]: ...
    async def get_by_id(self, *, route_id: UUID) -> Route | None: ...
    async def get_list_filtered(
        self,
        *,
        limit: int,
        offset: int,
        country_id: UUID | None = None,
        category: Category | None = None,
    ) -> Sequence[Route]: ...
    async def get_total_count(
        self, *, country_id: UUID | None = None, category: Category | None = None
    ) -> int: ...
    async def get_by_id_detailed(self, *, route_id: UUID) -> Route | None: ...
    async def get_hotels_count(self, *, route_id: UUID) -> int: ...
    async def get_restaurants_count(self, *, route_id: UUID) -> int: ...


class SqlAlchemyRouteRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_list(self, *, limit: int, offset: int) -> list[Route]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        stmt = (
            select(Route).order_by(Route.createdAt.desc()).offset(offset).limit(limit)
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, *, route_id: UUID) -> Route | None:
        stmt = select(Route).where(Route.id == route_id)
        result = await self._session.scalar(stmt)
        return result

    async def get_list_filtered(
        self,
        *,
        limit: int,
        offset: int,
        country_id: UUID | None = None,
        category: Category | None = None,
    ) -> list[Route]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        stmt = select(Route).options(joinedload(Route.country))

        if country_id:
            stmt = stmt.where(Route.countryId == country_id)
        if category:
            stmt = stmt.where(Route.category == category)

        stmt = stmt.order_by(Route.createdAt.desc()).offset(offset).limit(limit)

        result = await self._session.scalars(stmt)
        return list(result.unique().all())

    async def get_total_count(
        self, *, country_id: UUID | None = None, category: Category | None = None
    ) -> int:
        stmt = select(func.count(Route.id))

        if country_id:
            stmt = stmt.where(Route.countryId == country_id)
        if category:
            stmt = stmt.where(Route.category == category)

        result = await self._session.scalar(stmt)
        return result or 0

    async def get_by_id_detailed(self, *, route_id: UUID) -> Route | None:
        stmt = (
            select(Route)
            .where(Route.id == route_id)
            .options(
                joinedload(Route.country),
                joinedload(Route.route_images),
                joinedload(Route.amal_templates),
            )
        )
        result = await self._session.scalar(stmt)
        return result

    async def get_hotels_count(self, *, route_id: UUID) -> int:
        stmt = select(func.count(Hotel.id)).where(Hotel.routeId == route_id)
        result = await self._session.scalar(stmt)
        return result or 0

    async def get_restaurants_count(self, *, route_id: UUID) -> int:
        stmt = select(func.count(Restaurant.id)).where(Restaurant.routeId == route_id)
        result = await self._session.scalar(stmt)
        return result or 0

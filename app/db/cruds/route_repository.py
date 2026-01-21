from __future__ import annotations

import datetime
from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.enums import Category
from app.db.models.route import Route


@runtime_checkable
class RouteRepository(Protocol):
    async def get_list(self, *, limit: int, offset: int) -> Sequence[Route]: ...
    async def get_by_id(self, *, route_id: UUID) -> Route | None: ...


class MockRouteRepository:
    async def get_list(self, *, limit: int, offset: int) -> Sequence[Route]:
        mock_routes = [
            Route(
                id=UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"),
                name="Hajj Route to Mecca",
                content="A spiritual journey to the holy city of Mecca",
                views=1500,
                routeUrl="https://example.com/hajj-route",
                category=Category.HAJJ,
                countryId=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                created_at=datetime.datetime(2020, 1, 1, 12, 0),
                updated_at=datetime.datetime(2020, 1, 1, 12, 0),
            ),
            Route(
                id=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                name="Umrah Pilgrimage",
                content="A blessed journey of Umrah to the sacred lands",
                views=890,
                routeUrl="https://example.com/umrah-route",
                category=Category.UMRAH,
                countryId=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                created_at=datetime.datetime(2020, 2, 1, 12, 0),
                updated_at=datetime.datetime(2020, 2, 1, 12, 0),
            ),
            Route(
                id=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                name="Historical Islamic Sites",
                content="Explore the rich history of Islamic civilization",
                views=2340,
                routeUrl="https://example.com/history-route",
                category=Category.HISTORY,
                countryId=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                created_at=datetime.datetime(2020, 3, 1, 12, 0),
                updated_at=datetime.datetime(2020, 3, 1, 12, 0),
            ),
        ]
        paged_routes = mock_routes[offset : offset + limit]
        return paged_routes

    async def get_by_id(self, *, route_id: UUID) -> Route | None:
        mock_routes = [
            Route(
                id=UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"),
                name="Hajj Route to Mecca",
                content="A spiritual journey to the holy city of Mecca",
                views=1500,
                routeUrl="https://example.com/hajj-route",
                category=Category.HAJJ,
                countryId=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                created_at=datetime.datetime(2020, 1, 1, 12, 0),
                updated_at=datetime.datetime(2020, 1, 1, 12, 0),
            ),
            Route(
                id=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                name="Umrah Pilgrimage",
                content="A blessed journey of Umrah to the sacred lands",
                views=890,
                routeUrl="https://example.com/umrah-route",
                category=Category.UMRAH,
                countryId=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                created_at=datetime.datetime(2020, 2, 1, 12, 0),
                updated_at=datetime.datetime(2020, 2, 1, 12, 0),
            ),
            Route(
                id=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                name="Historical Islamic Sites",
                content="Explore the rich history of Islamic civilization",
                views=2340,
                routeUrl="https://example.com/history-route",
                category=Category.HISTORY,
                countryId=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                created_at=datetime.datetime(2020, 3, 1, 12, 0),
                updated_at=datetime.datetime(2020, 3, 1, 12, 0),
            ),
        ]
        for route in mock_routes:
            if route.id == route_id:
                return route
        return None


class SqlAlchemyRouteRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_list(self, *, limit: int, offset: int) -> list[Route]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        stmt = (
            select(Route).order_by(Route.created_at.desc()).offset(offset).limit(limit)
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, *, route_id: UUID) -> Route | None:
        stmt = select(Route).where(Route.id == route_id)
        result = await self._session.scalar(stmt)
        return result

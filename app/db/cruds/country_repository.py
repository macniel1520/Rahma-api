from __future__ import annotations

import datetime
from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.country import Country
from app.db.models.route import Route


@runtime_checkable
class CountryRepository(Protocol):
    async def get_list(self, *, limit: int, offset: int) -> Sequence[Country]: ...
    async def get_by_id(self, *, country_id: UUID) -> Country | None: ...
    async def get_routes_count(self, *, country_id: UUID) -> int: ...
    async def get_routes_counts(
        self, *, country_ids: list[UUID]
    ) -> list[tuple[UUID, int]]: ...
    async def get_list_with_routes_count(
        self, *, limit: int, offset: int
    ) -> Sequence[Country]: ...
    async def get_total_count(self) -> int: ...


class MockCountryRepository:
    async def get_list(self, *, limit: int, offset: int) -> Sequence[Country]:
        mock_countries = [
            Country(
                id=UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"),
                name="Turkey",
                photoUrl="https://example.com/turkey.jpg",
                createdAt=datetime.datetime(2020, 1, 1, 12, 0),
            ),
            Country(
                id=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                name="Germany",
                photoUrl="https://example.com/germany.jpg",
                createdAt=datetime.datetime(2020, 2, 1, 12, 0),
            ),
            Country(
                id=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                name="France",
                photoUrl="https://example.com/france.jpg",
                createdAt=datetime.datetime(2020, 3, 1, 12, 0),
            ),
        ]
        paged_countries = mock_countries[offset : offset + limit]
        return paged_countries

    async def get_by_id(self, *, country_id: UUID) -> Country | None:
        mock_countries = [
            Country(
                id=UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"),
                name="Turkey",
                photoUrl="https://example.com/turkey.jpg",
                createdAt=datetime.datetime(2020, 1, 1, 12, 0),
            ),
            Country(
                id=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                name="Germany",
                photoUrl="https://example.com/germany.jpg",
                createdAt=datetime.datetime(2020, 2, 1, 12, 0),
            ),
            Country(
                id=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                name="France",
                photoUrl="https://example.com/france.jpg",
                createdAt=datetime.datetime(2020, 3, 1, 12, 0),
            ),
        ]
        for country in mock_countries:
            if country.id == country_id:
                return country
        return None

    async def get_routes_count(self, *, country_id: UUID) -> int:
        # Mock route counts for each country
        mock_route_counts = {
            UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"): 5,  # Turkey
            UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"): 3,  # Germany
            UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"): 2,  # France
        }
        return mock_route_counts.get(country_id, 0)

    async def get_routes_counts(
        self, *, country_ids: list[UUID]
    ) -> list[tuple[UUID, int]]:
        # Mock route counts for each country
        mock_route_counts = {
            UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"): 5,  # Turkey
            UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"): 3,  # Germany
            UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"): 2,  # France
        }
        return [
            (country_id, mock_route_counts.get(country_id, 0))
            for country_id in country_ids
        ]

    async def get_list_with_routes_count(
        self, *, limit: int, offset: int
    ) -> Sequence[Country]:
        mock_countries = [
            Country(
                id=UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"),
                name="Turkey",
                photoUrl="https://example.com/turkey.jpg",
                createdAt=datetime.datetime(2020, 1, 1, 12, 0),
            ),
            Country(
                id=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                name="Germany",
                photoUrl="https://example.com/germany.jpg",
                createdAt=datetime.datetime(2020, 2, 1, 12, 0),
            ),
            Country(
                id=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                name="France",
                photoUrl="https://example.com/france.jpg",
                createdAt=datetime.datetime(2020, 3, 1, 12, 0),
            ),
        ]

        # Add routesCount to each country
        route_counts = {
            UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"): 5,  # Turkey
            UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"): 3,  # Germany
            UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"): 2,  # France
        }

        for country in mock_countries:
            country.routesCount = route_counts.get(country.id, 0)

        paged_countries = mock_countries[offset : offset + limit]
        return paged_countries

    async def get_total_count(self) -> int:
        return 3  # Mock total count


class SqlAlchemyCountryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_list(self, *, limit: int, offset: int) -> list[Country]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        stmt = (
            select(Country)
            .order_by(Country.createdAt.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, *, country_id: UUID) -> Country | None:
        stmt = select(Country).where(Country.id == country_id)
        result = await self._session.scalar(stmt)
        return result

    async def get_routes_count(self, *, country_id: UUID) -> int:
        stmt = select(func.count(Route.id)).where(Route.countryId == country_id)
        result = await self._session.scalar(stmt)
        return result or 0

    async def get_routes_counts(
        self, *, country_ids: list[UUID]
    ) -> list[tuple[UUID, int]]:
        if not country_ids:
            return []

        stmt = (
            select(Route.countryId, func.count(Route.id).label("routes_count"))
            .where(Route.countryId.in_(country_ids))
            .group_by(Route.countryId)
        )

        result = await self._session.execute(stmt)
        return [(row.countryId, row.routes_count) for row in result.all()]

    async def get_list_with_routes_count(
        self, *, limit: int, offset: int
    ) -> list[Country]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        # Subquery to get routes count per country
        routes_count_subq = (
            select(Route.countryId, func.count(Route.id).label("routes_count"))
            .group_by(Route.countryId)
            .subquery()
        )

        stmt = (
            select(
                Country,
                func.coalesce(routes_count_subq.c.routes_count, 0).label("routesCount"),
            )
            .outerjoin(routes_count_subq, Country.id == routes_count_subq.c.countryId)
            .order_by(Country.createdAt.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        countries_with_counts = result.all()

        # Add routesCount as attribute to Country objects
        countries = []
        for country, routes_count in countries_with_counts:
            country.routesCount = routes_count
            countries.append(country)

        return countries

    async def get_total_count(self) -> int:
        stmt = select(func.count(Country.id))
        result = await self._session.scalar(stmt)
        return result or 0

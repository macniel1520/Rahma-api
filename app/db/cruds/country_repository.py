from __future__ import annotations

import datetime
from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.country import Country


@runtime_checkable
class CountryRepository(Protocol):
    async def get_list(self, *, limit: int, offset: int) -> Sequence[Country]: ...
    async def get_by_id(self, *, country_id: UUID) -> Country | None: ...


class MockCountryRepository:
    async def get_list(self, *, limit: int, offset: int) -> Sequence[Country]:
        mock_countries = [
            Country(
                id=UUID("b9d6c522-2e4a-4a5d-9e5f-05410d7e13e9"),
                name="Turkey",
                photoUrl="https://example.com/turkey.jpg",
                routesCount=10,
                createdAt=datetime.datetime(2020, 1, 1, 12, 0),
            ),
            Country(
                id=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                name="Germany",
                photoUrl="https://example.com/germany.jpg",
                routesCount=8,
                createdAt=datetime.datetime(2020, 2, 1, 12, 0),
            ),
            Country(
                id=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                name="France",
                photoUrl="https://example.com/france.jpg",
                routesCount=12,
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
                routesCount=10,
                createdAt=datetime.datetime(2020, 1, 1, 12, 0),
            ),
            Country(
                id=UUID("1e43fadd-1345-4413-b83d-1662b0ba47e8"),
                name="Germany",
                photoUrl="https://example.com/germany.jpg",
                routesCount=8,
                createdAt=datetime.datetime(2020, 2, 1, 12, 0),
            ),
            Country(
                id=UUID("f1e71c81-b4e2-433e-9571-60186a9728d8"),
                name="France",
                photoUrl="https://example.com/france.jpg",
                routesCount=12,
                createdAt=datetime.datetime(2020, 3, 1, 12, 0),
            ),
        ]
        for country in mock_countries:
            if country.id == country_id:
                return country
        return None


class SqlAlchemyCountryRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_list(self, *, limit: int, offset: int) -> list[Country]:
        if offset < 0:
            offset = 0
        limit = max(1, min(limit, 100))

        stmt = (
            select(Country)
            .order_by(Country.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get_by_id(self, *, country_id: UUID) -> Country | None:
        stmt = select(Country).where(Country.id == country_id)
        result = await self._session.scalar(stmt)
        return result

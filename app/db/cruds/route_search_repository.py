from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.amal_template import AmalTemplate
from app.db.models.hotel import Hotel
from app.db.models.restaurant import Restaurant
from app.db.models.route import Route


@runtime_checkable
class RouteSearchRepository(Protocol):
    async def search_hotels_by_route(
        self, *, route_id: UUID, limit: int = 5
    ) -> Sequence[Hotel]: ...
    async def search_restaurants_by_route(
        self, *, route_id: UUID, limit: int = 5
    ) -> Sequence[Restaurant]: ...
    async def search_amal_templates_by_route(
        self, *, route_id: UUID, limit: int = 5
    ) -> Sequence[AmalTemplate]: ...
    async def find_route_by_keywords(self, *, keywords: list[str]) -> Route | None: ...


class SqlAlchemyRouteSearchRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def search_hotels_by_route(
        self, *, route_id: UUID, limit: int = 5
    ) -> list[Hotel]:
        """Поиск лучших отелей по маршруту (сортировка по рейтингу)"""
        stmt = (
            select(Hotel)
            .where(Hotel.routeId == route_id)
            .options(joinedload(Hotel.location))
            .order_by(Hotel.avgScore.desc())
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return list(result.unique().all())

    async def search_restaurants_by_route(
        self, *, route_id: UUID, limit: int = 5
    ) -> list[Restaurant]:
        """Поиск лучших ресторанов по маршруту (сортировка по рейтингу)"""
        stmt = (
            select(Restaurant)
            .where(Restaurant.routeId == route_id)
            .order_by(Restaurant.avgScore.desc())
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def search_amal_templates_by_route(
        self, *, route_id: UUID, limit: int = 5
    ) -> list[AmalTemplate]:
        """Поиск шаблонов амалов по маршруту"""
        stmt = (
            select(AmalTemplate)
            .where(AmalTemplate.routeId == route_id)
            .order_by(AmalTemplate.createdAt.desc())
            .limit(limit)
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def find_route_by_keywords(self, *, keywords: list[str]) -> Route | None:
        """Поиск маршрута по ключевым словам с учетом синонимов"""
        from sqlalchemy import or_

        if not keywords:
            return None

        # Расширяем ключевые слова синонимами
        expanded_keywords = []
        for keyword in keywords:
            keyword_lower = keyword.lower()
            expanded_keywords.append(keyword_lower)

            # Добавляем синонимы для известных мест
            if keyword_lower in ["мекка", "mecca", "mekka"]:
                expanded_keywords.extend(
                    ["saudi", "arabia", "саудовская", "аравия", "хадж", "hajj"]
                )
            elif keyword_lower in ["медина", "medina", "madina"]:
                expanded_keywords.extend(
                    ["saudi", "arabia", "саудовская", "аравия", "умра", "umrah"]
                )
            elif keyword_lower in ["хадж", "hajj", "hadj"]:
                expanded_keywords.extend(
                    ["мекка", "mecca", "mekka", "медина", "medina"]
                )
            elif keyword_lower in ["умра", "umrah", "umra"]:
                expanded_keywords.extend(["медина", "medina", "мекка", "mecca"])

        # Убираем дубликаты
        expanded_keywords = list(set(expanded_keywords))

        # Создаем условие ИЛИ для поиска по ключевым словам
        search_conditions = []
        for keyword in expanded_keywords:
            search_conditions.append(Route.name.ilike(f"%{keyword}%"))
            search_conditions.append(Route.content.ilike(f"%{keyword}%"))

        # Также ищем по названию страны
        stmt = (
            select(Route)
            .join(Route.country)
            .where(or_(*search_conditions))
            .options(
                joinedload(Route.country),
                joinedload(Route.amal_templates),
                joinedload(Route.hotels).joinedload(Hotel.location),
                joinedload(Route.restaurants),
            )
            .limit(1)
        )

        result = await self._session.scalar(stmt)
        return result

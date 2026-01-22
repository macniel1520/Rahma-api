from uuid import UUID

from app.api.v1.exceptions import resource_not_found_exc
from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.route_schema import RouteDetailRead, RouteRead
from app.db.cruds.route_repository import RouteRepository
from app.db.models.enums import Category


class RouteService:
    def __init__(self, repo: RouteRepository):
        self._repo = repo

    async def list(
        self,
        *,
        limit: int,
        offset: int,
        country_id: UUID | None = None,
        category: Category | None = None,
    ) -> LimitOffsetWrapper[RouteRead]:
        routes = await self._repo.get_list_filtered(
            limit=limit, offset=offset, country_id=country_id, category=category
        )
        total_count = await self._repo.get_total_count(
            country_id=country_id, category=category
        )

        # Populate routesCount for each country's routes
        country_ids = {route.country.id for route in routes if route.country}
        if country_ids:
            from app.db.cruds.country_repository import SqlAlchemyCountryRepository

            country_repo = SqlAlchemyCountryRepository(self._repo._session)
            routes_counts = await country_repo.get_routes_counts(
                country_ids=list(country_ids)
            )

            # Create a mapping of country_id -> routes_count
            routes_count_map = {
                country_id: count for country_id, count in routes_counts
            }

            # Set routesCount on each country
            for route in routes:
                if route.country and route.country.id in routes_count_map:
                    route.country.routesCount = routes_count_map[route.country.id]

        return LimitOffsetWrapper(
            count=total_count,
            items=[RouteRead.model_validate(route) for route in routes],
        )

    async def get(self, *, route_id: UUID) -> RouteRead:
        route = await self._repo.get_by_id(route_id=route_id)

        if route is None:
            raise resource_not_found_exc("Route", str(route_id))

        return RouteRead.model_validate(route)

    async def get_detail(self, *, route_id: UUID) -> RouteDetailRead:
        route = await self._repo.get_by_id_detailed(route_id=route_id)

        if route is None:
            raise resource_not_found_exc("Route", str(route_id))

        hotels_count = await self._repo.get_hotels_count(route_id=route_id)
        restaurants_count = await self._repo.get_restaurants_count(route_id=route_id)

        # Build the route data with all required fields
        route_data = {
            **RouteRead.model_validate(route).model_dump(),
            "hotelsCount": hotels_count,
            "restaurantsCount": restaurants_count,
            "images": route.route_images,
            "amalTemplates": route.amal_templates,
        }

        return RouteDetailRead.model_validate(route_data)

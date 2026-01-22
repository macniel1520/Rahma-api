from uuid import UUID

from app.api.v1.exceptions import resource_not_found_exc
from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.restaurant_schema import RestaurantRead
from app.db.cruds.restaurant_repository import RestaurantRepository
from app.db.cruds.route_repository import RouteRepository


class RestaurantService:
    def __init__(
        self, repo: RestaurantRepository, route_repo: RouteRepository | None = None
    ):
        self._repo = repo
        self._route_repo = route_repo

    async def list_by_route(
        self,
        *,
        route_id: UUID,
        limit: int,
        offset: int,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> LimitOffsetWrapper[RestaurantRead]:
        if self._route_repo:
            route = await self._route_repo.get_by_id(route_id=route_id)
            if route is None:
                raise resource_not_found_exc("Route", str(route_id))

        restaurants = await self._repo.get_list_by_route(
            route_id=route_id,
            limit=limit,
            offset=offset,
            min_score=min_score,
            max_score=max_score,
        )
        total_count = await self._repo.get_total_count(
            route_id=route_id, min_score=min_score, max_score=max_score
        )

        return LimitOffsetWrapper(
            count=total_count,
            items=[
                RestaurantRead.model_validate(restaurant) for restaurant in restaurants
            ],
        )

from uuid import UUID

from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.restaurant_schema import RestaurantRead
from app.db.cruds.restaurant_repository import RestaurantRepository


class RestaurantService:
    def __init__(self, repo: RestaurantRepository):
        self._repo = repo

    async def list_by_route(
        self,
        *,
        route_id: UUID,
        limit: int,
        offset: int,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> LimitOffsetWrapper[RestaurantRead]:
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

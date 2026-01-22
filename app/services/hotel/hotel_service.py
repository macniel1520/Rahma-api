from uuid import UUID

from app.api.v1.exceptions import resource_not_found_exc
from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.hotel_schema import HotelRead
from app.db.cruds.hotel_repository import HotelRepository
from app.db.cruds.route_repository import RouteRepository


class HotelService:
    def __init__(self, repo: HotelRepository, route_repo: RouteRepository | None = None):
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
    ) -> LimitOffsetWrapper[HotelRead]:
        if self._route_repo:
            route = await self._route_repo.get_by_id(route_id=route_id)
            if route is None:
                raise resource_not_found_exc("Route", str(route_id))

        hotels = await self._repo.get_list_by_route(
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
            items=[HotelRead.model_validate(hotel) for hotel in hotels],
        )

from uuid import UUID

from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.hotel_schema import HotelRead
from app.db.cruds.hotel_repository import HotelRepository


class HotelService:
    def __init__(self, repo: HotelRepository):
        self._repo = repo

    async def list_by_route(
        self,
        *,
        route_id: UUID,
        limit: int,
        offset: int,
        min_score: float | None = None,
        max_score: float | None = None,
    ) -> LimitOffsetWrapper[HotelRead]:
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

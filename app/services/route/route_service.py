from uuid import UUID

from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.route_schema import RouteRead
from app.db.cruds.route_repository import RouteRepository


class RouteService:
    def __init__(self, repo: RouteRepository):
        self._repo = repo

    async def list(self, *, limit: int, offset: int) -> LimitOffsetWrapper[RouteRead]:
        routes = await self._repo.get_list(limit=limit, offset=offset)

        return LimitOffsetWrapper(
            count=len(routes),
            items=[RouteRead.model_validate(route) for route in routes],
        )

    async def get(self, *, route_id: UUID) -> RouteRead:
        route = await self._repo.get_by_id(route_id=route_id)

        return RouteRead.model_validate(route)

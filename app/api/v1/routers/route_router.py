import uuid

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.hotel_schema import HotelRead
from app.api.v1.schemas.sabil.restaurant_schema import RestaurantRead
from app.api.v1.schemas.sabil.route_schema import RouteDetailRead, RouteRead
from app.db.cruds.hotel_repository import SqlAlchemyHotelRepository
from app.db.cruds.restaurant_repository import SqlAlchemyRestaurantRepository
from app.db.cruds.route_repository import SqlAlchemyRouteRepository
from app.db.engine import get_session
from app.db.models.enums import Category
from app.services.hotel.hotel_service import HotelService
from app.services.restaurant.restaurant_service import RestaurantService
from app.services.route.route_service import RouteService

router = APIRouter(prefix="/routes", tags=["routes"])


def get_route_service(session: AsyncSession = Depends(get_session)) -> RouteService:
    return RouteService(repo=SqlAlchemyRouteRepository(session=session))


def get_hotel_service(session: AsyncSession = Depends(get_session)) -> HotelService:
    return HotelService(repo=SqlAlchemyHotelRepository(session=session))


def get_restaurant_service(
    session: AsyncSession = Depends(get_session),
) -> RestaurantService:
    return RestaurantService(repo=SqlAlchemyRestaurantRepository(session=session))


@router.get("", response_model=LimitOffsetWrapper[RouteRead])
async def get_routes(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    country: uuid.UUID | None = Query(None, description="Filter by country ID"),
    category: Category | None = Query(None, description="Filter by category"),
    service: RouteService = Depends(get_route_service),
) -> LimitOffsetWrapper[RouteRead]:
    return await service.list(
        limit=limit, offset=offset, country_id=country, category=category
    )


@router.get("/{route_uuid}", response_model=RouteDetailRead)
async def get_route(
    route_uuid: uuid.UUID = Path(..., description="The UUID of the route"),
    service: RouteService = Depends(get_route_service),
) -> RouteDetailRead:
    return await service.get_detail(route_id=route_uuid)


@router.get("/{route_uuid}/hotels", response_model=LimitOffsetWrapper[HotelRead])
async def get_route_hotels(
    route_uuid: uuid.UUID = Path(..., description="The UUID of the route"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_score: float | None = Query(
        None, ge=0.0, le=5.0, description="Minimum average score"
    ),
    max_score: float | None = Query(
        None, ge=0.0, le=5.0, description="Maximum average score"
    ),
    service: HotelService = Depends(get_hotel_service),
) -> LimitOffsetWrapper[HotelRead]:
    return await service.list_by_route(
        route_id=route_uuid,
        limit=limit,
        offset=offset,
        min_score=min_score,
        max_score=max_score,
    )


@router.get(
    "/{route_uuid}/restaurants", response_model=LimitOffsetWrapper[RestaurantRead]
)
async def get_route_restaurants(
    route_uuid: uuid.UUID = Path(..., description="The UUID of the route"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    min_score: float | None = Query(
        None, ge=0.0, le=5.0, description="Minimum average score"
    ),
    max_score: float | None = Query(
        None, ge=0.0, le=5.0, description="Maximum average score"
    ),
    service: RestaurantService = Depends(get_restaurant_service),
) -> LimitOffsetWrapper[RestaurantRead]:
    return await service.list_by_route(
        route_id=route_uuid,
        limit=limit,
        offset=offset,
        min_score=min_score,
        max_score=max_score,
    )

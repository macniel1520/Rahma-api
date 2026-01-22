import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.common.error_schema import ErrorResponse
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
    return HotelService(
        repo=SqlAlchemyHotelRepository(session=session),
        route_repo=SqlAlchemyRouteRepository(session=session),
    )


def get_restaurant_service(
    session: AsyncSession = Depends(get_session),
) -> RestaurantService:
    return RestaurantService(
        repo=SqlAlchemyRestaurantRepository(session=session),
        route_repo=SqlAlchemyRouteRepository(session=session),
    )


@router.get(
    "",
    response_model=LimitOffsetWrapper[RouteRead],
    summary="Получить список маршрутов",
    description=(
        "Возвращает список маршрутов с пагинацией.\n\n"
        "Поддерживается пагинация через механизм **limit/offset**:\n"
        "- `limit` задаёт размер страницы (максимум 100)\n"
        "- `offset` указывает стартовую позицию (изначально: 0)\n\n"
        "Можно фильтровать маршруты по стране и их категории."
    ),
    response_description="Список маршрутов с пагинацией",
)
async def get_routes(
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Размер страницы",
            examples={
                "default": {"summary": "По умолчанию", "value": 20},
                "max": {"summary": "Максимальное значение", "value": 100},
            },
        ),
    ] = 20,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Количество элементов для пропуска",
            examples={
                "default": {"summary": "По умолчанию", "value": 0},
                "nextPage": {"summary": "Следующая страница", "value": 20},
            },
        ),
    ] = 0,
    country: Annotated[
        uuid.UUID | None,
        Query(
            description="Идентификатор страны (UUID)",
            examples={
                "default": {"summary": "По умолчанию", "value": None},
                "example": {
                    "summary": "Пример идентификатора страны",
                    "value": "123e4567-e89b-12d3-a456-426614174000",
                },
            },
        ),
    ] = None,
    category: Annotated[
        Category | None,
        Query(
            description="Категория маршрута",
            examples={
                "example": {"summary": "Пример категории маршрута", "value": "HAJJ"},
                "default": {"summary": "По умолчанию", "value": None},
            },
        ),
    ] = None,
    service: RouteService = Depends(get_route_service),
) -> LimitOffsetWrapper[RouteRead]:
    return await service.list(
        limit=limit, offset=offset, country_id=country, category=category
    )


@router.get(
    "/{route_uuid}",
    response_model=RouteDetailRead,
    summary="Получить маршрут по ID",
    description=(
        "Возвращает маршрут по его идентификатору.\n\n"
        "Поле `hotelsCount` содержит количество отелей в маршруте.\n\n"
        "Поле `restaurantsCount` содержит количество ресторанов в маршруте.\n\n"
        "Поле `images` содержит список изображений.\n\n"
        "Поле `amalTemplates` содержит список шаблонов для создания амалов.\n\n"
    ),
    response_description="Маршрут с подробной информацией",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Маршрут не найден",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации параметров запроса",
        },
    },
)
async def get_route(
    route_uuid: uuid.UUID = Path(
        ...,
        description="Идентификатор маршрута (UUID)",
        examples={
            "default": {
                "summary": "Пример идентификатора маршрута",
                "value": "123e4567-e89b-12d3-a456-426614174000",
            },
        },
    ),
    service: RouteService = Depends(get_route_service),
) -> RouteDetailRead:
    return await service.get_detail(route_id=route_uuid)


@router.get(
    "/{route_uuid}/hotels",
    response_model=LimitOffsetWrapper[HotelRead],
    summary="Получить список отелей маршрута",
    description=(
        "Возвращает список отелей для указанного маршрута с пагинацией.\n\n"
        "Поддерживается фильтрация по рейтингу параметрами `min_score` и `max_score`."
    ),
    response_description="Список отелей с пагинацией",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Маршрут не найден",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации параметров запроса",
        },
    },
)
async def get_route_hotels(
    route_uuid: uuid.UUID = Path(
        ...,
        description="Идентификатор маршрута (UUID)",
        examples={
            "default": {
                "summary": "Пример идентификатора маршрута",
                "value": "123e4567-e89b-12d3-a456-426614174000",
            },
        },
    ),
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Размер страницы",
            examples={
                "default": {"summary": "По умолчанию", "value": 20},
                "max": {"summary": "Максимальное значение", "value": 100},
            },
        ),
    ] = 20,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Количество элементов для пропуска",
            examples={
                "default": {"summary": "По умолчанию", "value": 0},
                "nextPage": {"summary": "Следующая страница", "value": 20},
            },
        ),
    ] = 0,
    min_score: Annotated[
        float | None,
        Query(
            ge=0.0,
            le=5.0,
            description="Минимальный средний рейтинг",
            examples={
                "default": {"summary": "По умолчанию", "value": None},
                "example": {
                    "summary": "Пример минимального среднего рейтинга",
                    "value": 0.0,
                },
            },
        ),
    ] = None,
    max_score: Annotated[
        float | None,
        Query(
            ge=0.0,
            le=5.0,
            description="Максимальный средний рейтинг",
            examples={
                "default": {"summary": "По умолчанию", "value": None},
                "example": {
                    "summary": "Пример максимального среднего рейтинга",
                    "value": 5.0,
                },
            },
        ),
    ] = None,
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
    "/{route_uuid}/restaurants",
    response_model=LimitOffsetWrapper[RestaurantRead],
    summary="Получить список ресторанов маршрута",
    description=(
        "Возвращает список ресторанов для указанного маршрута с пагинацией.\n\n"
        "Поддерживается фильтрация по рейтингу параметрами `min_score` и `max_score`."
    ),
    response_description="Список ресторанов с пагинацией",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Маршрут не найден",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации параметров запроса",
        },
    },
)
async def get_route_restaurants(
    route_uuid: uuid.UUID = Path(
        ...,
        description="Идентификатор маршрута (UUID)",
        examples={
            "default": {
                "summary": "Пример идентификатора маршрута",
                "value": "123e4567-e89b-12d3-a456-426614174000",
            },
        },
    ),
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Размер страницы",
            examples={
                "default": {"summary": "По умолчанию", "value": 20},
                "max": {"summary": "Максимальное значение", "value": 100},
            },
        ),
    ] = 20,
    offset: Annotated[
        int,
        Query(
            ge=0,
            description="Количество элементов для пропуска",
            examples={
                "default": {"summary": "По умолчанию", "value": 0},
                "nextPage": {"summary": "Следующая страница", "value": 20},
            },
        ),
    ] = 0,
    min_score: Annotated[
        float | None,
        Query(
            ge=0.0,
            le=5.0,
            description="Минимальный средний рейтинг",
            examples={
                "default": {"summary": "По умолчанию", "value": None},
                "example": {
                    "summary": "Пример минимального среднего рейтинга",
                    "value": 0.0,
                },
            },
        ),
    ] = None,
    max_score: Annotated[
        float | None,
        Query(
            ge=0.0,
            le=5.0,
            description="Максимальный средний рейтинг",
            examples={
                "default": {"summary": "По умолчанию", "value": None},
                "example": {
                    "summary": "Пример максимального среднего рейтинга",
                    "value": 5.0,
                },
            },
        ),
    ] = None,
    service: RestaurantService = Depends(get_restaurant_service),
) -> LimitOffsetWrapper[RestaurantRead]:
    return await service.list_by_route(
        route_id=route_uuid,
        limit=limit,
        offset=offset,
        min_score=min_score,
        max_score=max_score,
    )

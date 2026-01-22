import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.common.error_schema import ErrorResponse
from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.country_schema import CountryRead
from app.db.cruds.country_repository import SqlAlchemyCountryRepository
from app.db.engine import get_session
from app.services.country.country_service import CountryService

router = APIRouter(prefix="/countries", tags=["countries"])


def get_country_service(session: AsyncSession = Depends(get_session)) -> CountryService:
    return CountryService(repo=SqlAlchemyCountryRepository(session=session))


@router.get(
    "",
    response_model=LimitOffsetWrapper[CountryRead],
    summary="Получить список стран",
    description=(
        "Возвращает список стран с пагинацией.\n\n"
        "Поддерживается пагинация через механизм **limit/offset**:\n"
        "- `limit` задаёт размер страницы (максимум 100)\n"
        "- `offset` указывает стартовую позицию (изначально: 0)\n\n"
        "Поле `routesCount` отображает количество маршрутов в стране."
    ),
    response_description="Список стран с пагинацией",
)
async def get_countries(
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
    service: CountryService = Depends(get_country_service),
) -> LimitOffsetWrapper[CountryRead]:
    return await service.list(limit=limit, offset=offset)


@router.get(
    "/{country_id}",
    response_model=CountryRead,
    summary="Получить страну по ID",
    description=(
        "Возвращает страну по её идентификатору.\n\n"
        "Поле `routesCount` всегда `null` при вызове этой ручки."
    ),
    response_description="Страна",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Страна не найдена",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Ошибка валидации параметров запроса",
        },
    },
)
async def get_country(
    country_id: uuid.UUID = Path(
        ...,
        description="Идентификатор страны (UUID)",
        examples={
            "default": {
                "summary": "Пример идентификатора страны",
                "value": "123e4567-e89b-12d3-a456-426614174000",
            },
        },
    ),
    service: CountryService = Depends(get_country_service),
) -> CountryRead:
    return await service.get(country_id=country_id)

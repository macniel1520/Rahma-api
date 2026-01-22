import uuid

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.country_schema import CountryRead
from app.db.cruds.country_repository import SqlAlchemyCountryRepository
from app.db.engine import get_session
from app.services.country.country_service import CountryService

router = APIRouter(prefix="/countries", tags=["countries"])


def get_country_service(session: AsyncSession = Depends(get_session)) -> CountryService:
    return CountryService(repo=SqlAlchemyCountryRepository(session=session))


@router.get("", response_model=LimitOffsetWrapper[CountryRead])
async def get_countries(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: CountryService = Depends(get_country_service),
) -> LimitOffsetWrapper[CountryRead]:
    return await service.list(limit=limit, offset=offset)


@router.get("/{country_id}", response_model=CountryRead)
async def get_country(
    country_id: uuid.UUID = Path(..., description="The ID of the country"),
    service: CountryService = Depends(get_country_service),
) -> CountryRead:
    return await service.get(country_id=country_id)

from uuid import UUID

from app.db.cruds.country_repository import CountryRepository
from app.db.services.country.exceptions import CountryNotFoundError
from app.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.schemas.sabil.country_schema import CountryRead


class CountryService:
    def __init__(self, repo: CountryRepository):
        self._repo = repo

    async def list(self, *, limit: int, offset: int) -> LimitOffsetWrapper[CountryRead]:
        countries = await self._repo.get_list(limit=limit, offset=offset)
        return LimitOffsetWrapper(
            count=len(countries),
            items=[CountryRead.model_validate(country) for country in countries],
        )

    async def get(self, *, country_id: UUID) -> CountryRead:
        country = await self._repo.get_by_id(country_id=country_id)
        if country is None:
            raise CountryNotFoundError(country_id)
        return CountryRead.model_validate(country)

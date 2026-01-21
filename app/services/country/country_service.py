from uuid import UUID

from app.api.v1.schemas.common.limit_offset_wrapper import LimitOffsetWrapper
from app.api.v1.schemas.sabil.country_schema import CountryRead
from app.db.cruds.country_repository import CountryRepository


class CountryService:
    def __init__(self, repo: CountryRepository):
        self._repo = repo

    async def list(self, *, limit: int, offset: int) -> LimitOffsetWrapper[CountryRead]:
        countries = await self._repo.get_list_with_routes_count(
            limit=limit, offset=offset
        )

        return LimitOffsetWrapper(
            count=len(countries),
            items=[CountryRead.model_validate(country) for country in countries],
        )

    async def get(self, *, country_id: UUID) -> CountryRead:
        country = await self._repo.get_by_id(country_id=country_id)

        return CountryRead.model_validate(country)

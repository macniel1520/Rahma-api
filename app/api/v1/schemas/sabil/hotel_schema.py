from pydantic import URL, Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.api.v1.schemas.sabil.location_schema import LocationRead


class HotelRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str
    description: str
    photoUrl: URL
    avgScore: float = Field(ge=0.0, le=5.0)
    scoreCount: int = Field(ge=0)
    avgPrice: float = Field(ge=0.0)
    location: LocationRead

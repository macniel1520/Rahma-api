from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin


class LocationRead(AttributeMixin):
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)

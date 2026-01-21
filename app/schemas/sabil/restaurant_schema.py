from pydantic import URL, Field

from app.db.models.enums import CostLevel
from app.schemas.common.attribute_mixin import AttributeMixin
from app.schemas.common.created_at_mixin import CreatedAtMixin
from app.schemas.common.uuid_mixin import UUIDMixin


class RestaurantRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str
    description: str
    photoUrl: URL
    avgScore: float = Field(ge=0.0, le=5.0)
    scoreCount: int = Field(ge=0)
    isHaram: bool
    costLevel: CostLevel

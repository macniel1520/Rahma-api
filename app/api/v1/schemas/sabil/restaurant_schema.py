from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.db.models.enums import CostLevel


class RestaurantRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str
    description: str
    photoUrl: str
    avgScore: float = Field(ge=0.0, le=5.0)
    scoreCount: int = Field(ge=0)
    isHaram: bool
    costLevel: CostLevel

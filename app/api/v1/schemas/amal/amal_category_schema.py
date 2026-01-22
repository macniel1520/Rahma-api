import uuid

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from pydantic import Field


class AmalCategoryRead(AttributeMixin, UUIDMixin):
    name: str = Field(
        ..., title="Название", description="Название категории", example="Намаз"
    )


class AmalCategoryCreate(AttributeMixin):
    id: uuid.UUID = Field(
        ...,
        title="ID",
        description="ID категории",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    name: str = Field(
        ..., title="Название", description="Название категории", example="Намаз"
    )

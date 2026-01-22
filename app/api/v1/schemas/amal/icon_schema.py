import uuid

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from pydantic import Field


class IconRead(AttributeMixin, UUIDMixin):
    url: str = Field(
        ...,
        title="URL",
        description="URL иконки",
        example="https://example.com/icon.png",
    )


class IconCreate(AttributeMixin):
    id: uuid.UUID = Field(
        ...,
        title="ID",
        description="ID иконки",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    url: str = Field(
        ...,
        title="URL",
        description="URL иконки",
        example="https://example.com/icon.png",
    )

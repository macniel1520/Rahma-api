import uuid

from pydantic import Field


class UUIDMixin:
    id: uuid.UUID = Field(
        ...,
        title="Уникальный идентификатор",
        description="Уникальный идентификатор объекта",
        example="123e4567-e89b-12d3-a456-426614174000",
    )

import datetime
import uuid

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from pydantic import Field


class AmalCompletionRead(AttributeMixin, UUIDMixin):
    amalId: uuid.UUID = Field(
        ...,
        title="ID",
        description="ID амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    date: datetime.date = Field(
        ..., title="Дата", description="Дата выполнения амала", example="2026-01-22"
    )
    completedAt: datetime.datetime = Field(
        ...,
        title="Дата завершения",
        description="Дата завершения амала",
        example="2026-01-22T20:15:00",
    )


class AmalCompletionCreate(AttributeMixin):
    id: uuid.UUID = Field(
        ...,
        title="ID",
        description="ID выполнения амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    amalId: uuid.UUID = Field(
        ...,
        title="ID",
        description="ID амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    date: datetime.date = Field(
        ..., title="Дата", description="Дата выполнения амала", example="2026-01-22"
    )
    completedAt: datetime.datetime = Field(
        ...,
        title="Дата завершения",
        description="Дата завершения амала",
        example="2026-01-22T20:15:00",
    )

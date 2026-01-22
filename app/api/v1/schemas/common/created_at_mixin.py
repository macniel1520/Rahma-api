import datetime

from pydantic import Field


class CreatedAtMixin:
    createdAt: datetime.datetime = Field(
        ...,
        title="Дата создания",
        description="Дата создания объекта",
        example="2026-01-22T10:13:03.823021Z",
    )

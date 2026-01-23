import datetime
import uuid

from pydantic import BaseModel, Field

from app.api.v1.schemas.amal.amal_category_schema import AmalCategoryRead
from app.api.v1.schemas.amal.amal_completion_schema import (
    AmalCompletionRead,
    AmalCompletionCreate,
)
from app.api.v1.schemas.amal.icon_schema import IconRead
from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.db.models.enums import ReccuringRule


class AmalRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    title: str = Field(
        ..., title="Название", description="Название амала", example="Намаз"
    )
    date: datetime.date = Field(
        ..., title="Дата", description="Дата амала", example="2026-01-22"
    )
    time: datetime.time = Field(
        ..., title="Время", description="Время амала", example="12:00:00"
    )
    reccuringRule: ReccuringRule = Field(
        ..., description="Правило повторения амала", example="daily"
    )
    amalCategoryId: uuid.UUID | None = Field(
        None,
        title="ID",
        description="ID категории амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    iconId: uuid.UUID | None = Field(
        None,
        title="ID",
        description="ID иконки амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    icon: IconRead | None = Field(None, title="Иконка", description="Иконка амала")
    category: AmalCategoryRead | None = Field(
        None, title="Категория", description="Категория амала"
    )


class AmalCreate(AttributeMixin):
    id: uuid.UUID = Field(
        ...,
        title="ID",
        description="ID амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    title: str = Field(
        ..., title="Название", description="Название амала", example="Намаз"
    )
    date: datetime.date = Field(
        ..., title="Дата", description="Дата амала", example="2026-01-22"
    )
    time: datetime.time = Field(
        ..., title="Время", description="Время амала", example="12:00:00"
    )
    reccuringRule: ReccuringRule = Field(
        ...,
        title="Правило повторения",
        description="Правило повторения амала",
        example="daily",
    )
    amalCategoryId: uuid.UUID | None = Field(
        None,
        title="ID",
        description="ID категории амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )
    iconId: uuid.UUID | None = Field(
        None,
        title="ID",
        description="ID иконки амала",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class AmalSyncRequest(BaseModel):
    amals: list[AmalCreate] = Field(
        default_factory=list,
        title="Амалы",
        description="Список амалов для создания или обновления.",
    )
    deletedAmalIds: list[uuid.UUID] = Field(
        default_factory=list, title="ID`s", description="Список ID амалов для удаления."
    )
    completions: list[AmalCompletionCreate] = Field(
        default_factory=list,
        title="Завершенные амалы",
        description="Список завершений амалов для создания или обновления.",
    )
    deletedCompletionIds: list[uuid.UUID] = Field(
        default_factory=list,
        title="ID`s",
        description="Список ID завершений амалов для удаления.",
    )


class AmalSyncResponse(AttributeMixin):
    amals: list[AmalRead] = Field(
        default_factory=list,
        title="Амалы",
        description="Список амалов для синхронизации.",
    )
    completions: list[AmalCompletionRead] = Field(
        default_factory=list,
        title="Завершенные амалы",
        description="Список завершений амалов для синхронизации.",
    )

import datetime
import uuid

from pydantic import BaseModel

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
    title: str
    date: datetime.date
    time: datetime.time
    reccuringRule: ReccuringRule
    amalCategoryId: uuid.UUID | None = None
    iconId: uuid.UUID | None = None
    icon: IconRead | None = None
    category: AmalCategoryRead | None = None


class AmalCreate(AttributeMixin):
    id: uuid.UUID
    title: str
    date: datetime.date
    time: datetime.time
    reccuringRule: ReccuringRule
    amalCategoryId: uuid.UUID | None = None
    iconId: uuid.UUID | None = None


class AmalSyncRequest(BaseModel):
    amals: list[AmalCreate] = []
    deletedAmalIds: list[uuid.UUID] = []
    completions: list[AmalCompletionCreate] = []
    deletedCompletionIds: list[uuid.UUID] = []


class AmalSyncResponse(AttributeMixin):
    amals: list[AmalRead]
    completions: list[AmalCompletionRead]
    categories: list[AmalCategoryRead]
    icons: list[IconRead]

import datetime
import uuid

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin


class AmalCompletionRead(AttributeMixin, UUIDMixin):
    amalId: uuid.UUID
    date: datetime.date
    completedAt: datetime.datetime


class AmalCompletionCreate(AttributeMixin):
    id: uuid.UUID
    amalId: uuid.UUID
    date: datetime.date
    completedAt: datetime.datetime

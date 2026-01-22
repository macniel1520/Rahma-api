import uuid

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin


class IconRead(AttributeMixin, UUIDMixin):
    url: str


class IconCreate(AttributeMixin):
    id: uuid.UUID
    url: str

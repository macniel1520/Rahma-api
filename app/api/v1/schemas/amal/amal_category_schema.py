import uuid

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin


class AmalCategoryRead(AttributeMixin, UUIDMixin):
    name: str


class AmalCategoryCreate(AttributeMixin):
    id: uuid.UUID
    name: str

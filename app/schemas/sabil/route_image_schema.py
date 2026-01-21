from app.schemas.common.attribute_mixin import AttributeMixin
from app.schemas.common.created_at_mixin import CreatedAtMixin
from app.schemas.common.uuid_mixin import UUIDMixin


class RouteImageRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    url: str

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin


class RouteImageRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    url: str

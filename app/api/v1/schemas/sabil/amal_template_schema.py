from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.db.models.enums import ReccuringRule


class AmalTemplateRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    title: str
    reccuringRule: ReccuringRule

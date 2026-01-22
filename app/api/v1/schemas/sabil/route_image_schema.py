from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin


class RouteImageRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    url: str = Field(
        ...,
        title="URL изображения",
        description="URL изображения в карусели у маршрута",
        example="https://s3.geometria.ru/rahma-test/routes/uuid/image1.png",
    )

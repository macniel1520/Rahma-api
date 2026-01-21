from typing import TYPE_CHECKING

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.db.models.enums import Category

if TYPE_CHECKING:
    from app.api.v1.schemas.sabil.route_schema import RouteRead


class CountryRead(UUIDMixin, AttributeMixin, CreatedAtMixin):
    name: str
    photoUrl: str
    routesCount: int | None = None


class CountryDetailRead(CountryRead):
    routes: list["RouteRead"]
    category: Category

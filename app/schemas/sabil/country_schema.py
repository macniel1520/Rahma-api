from typing import TYPE_CHECKING

from app.db.models.enums import Category
from app.schemas.common.attribute_mixin import AttributeMixin
from app.schemas.common.created_at_mixin import CreatedAtMixin
from app.schemas.common.uuid_mixin import UUIDMixin

if TYPE_CHECKING:
    from app.schemas.sabil.route_schema import RouteRead


class CountryRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str
    photoUrl: str
    routesCount: int


class CountryDetailRead(CountryRead):
    routes: list["RouteRead"]
    category: Category

from app.db.models.enums import Category
from app.schemas.common.attribute_mixin import AttributeMixin
from app.schemas.common.created_at_mixin import CreatedAtMixin
from app.schemas.common.uuid_mixin import UUIDMixin
from app.schemas.sabil.amal_template_schema import AmalTemplateRead
from app.schemas.sabil.country_schema import CountryRead
from app.schemas.sabil.route_image_schema import RouteImageRead


class RouteRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str
    content: str
    category: Category
    country: CountryRead


class RouteDetailRead(RouteRead):
    hotelsCount: int
    restaurantsCount: int
    images: list[RouteImageRead]
    amalTemplates: list[AmalTemplateRead]

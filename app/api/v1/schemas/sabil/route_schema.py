from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.api.v1.schemas.sabil.amal_template_schema import AmalTemplateRead
from app.api.v1.schemas.sabil.country_schema import CountryRead
from app.api.v1.schemas.sabil.route_image_schema import RouteImageRead
from app.db.models.enums import Category


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

from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.api.v1.schemas.sabil.amal_template_schema import AmalTemplateRead
from app.api.v1.schemas.sabil.country_schema import CountryRead
from app.api.v1.schemas.sabil.route_image_schema import RouteImageRead
from app.db.models.enums import Category


class RouteRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str = Field(
        ...,
        title="Название",
        description="Название маршрута",
        examples=["Хадж в Мекку", "Умра: 7 дней", "Медина и Мекка"],
    )
    content: str = Field(
        ...,
        title="Описание",
        description="Описание маршрута",
        example="Хадж в Мекку - это поездка в Мекку, Саудовская Аравия, для выполнения хаджа. Хадж - это одно из пяти обязательных пунктов хаджджа.",
    )
    category: Category = Field(
        ...,
        title="Категория",
        description="Категория маршрута",
        examples=["hajj", "umrah", "history"],
    )
    country: CountryRead = Field(
        ...,
        title="Страна",
        description="Страна маршрута",
    )


class RouteDetailRead(RouteRead):
    hotelsCount: int = Field(
        ...,
        title="Количество отелей",
        description="Количество отелей в маршруте",
        example=15,
    )
    restaurantsCount: int = Field(
        ...,
        title="Количество ресторанов",
        description="Количество ресторанов в маршруте",
        example=6,
    )
    images: list[RouteImageRead] = Field(
        ...,
        title="Изображения",
        description="Изображения в карусели у маршрута",
    )
    amalTemplates: list[AmalTemplateRead] = Field(
        ...,
        title="Шаблоны амалов",
        description="Шаблоны амалов в маршруте для быстрого создания",
    )

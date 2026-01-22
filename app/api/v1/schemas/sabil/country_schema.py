from typing import TYPE_CHECKING

from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.db.models.enums import Category

if TYPE_CHECKING:
    from app.api.v1.schemas.sabil.route_schema import RouteRead


class CountryRead(UUIDMixin, AttributeMixin, CreatedAtMixin):
    name: str = Field(
        ...,
        title="Название",
        description="Название страны",
        examples=["Саудовская Аравия", "Турция", "Египет"],
    )
    photoUrl: str = Field(
        ...,
        title="URL фото",
        description="URL фотографии страны",
        example="https://s3.geometria.ru/rahma-test/countries/Saudi_Arabia.png",
    )
    routesCount: int | None = Field(
        default=None,
        title="Количество маршрутов",
        description="Количество маршрутов в этой стране",
        example=35,
    )


class CountryDetailRead(CountryRead):
    routes: list["RouteRead"] = Field(
        ...,
        title="Список маршрутов",
        description="Список маршрутов в стране",
    )
    category: Category = Field(
        ...,
        title="Категория",
        description="Категория маршрутов в стране",
        examples=["hajj", "umrah", "history"],
    )

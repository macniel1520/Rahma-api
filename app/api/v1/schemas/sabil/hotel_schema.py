from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.api.v1.schemas.sabil.location_schema import LocationRead


class HotelRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str = Field(
        ..., title="Название", description="Название отеля", example="Hotel Al Faisal"
    )
    description: str = Field(
        ...,
        title="Описание",
        description="Описание отеля",
        example="Hotel Al Faisal is a 5-star hotel located in the heart of Riyadh, Saudi Arabia.",
    )
    photoUrl: str = Field(
        ...,
        title="URL фото",
        description="URL фото отеля",
        example="https://s3.geometria.ru/rahma-test/hotels/Hotel_Al_Faisal.png",
    )
    avgScore: float = Field(
        ge=0.0,
        le=5.0,
        title="Средний балл",
        description="Средний балл отеля",
        example=4.5,
    )
    scoreCount: int = Field(
        ge=0,
        title="Количество оценок",
        description="Количество оценок отеля",
        example=2100,
    )
    avgPrice: float = Field(
        ge=0.0,
        title="Средняя цена",
        description="Средняя цена отеля",
        example=50,
    )
    location: LocationRead = Field(
        ...,
        title="Локация",
        description="Локация отеля",
    )

from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.db.models.enums import CostLevel


class RestaurantRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    name: str = Field(
        ...,
        title="Название",
        description="Название ресторана",
        examples=[
            "Restaurant Al Faisal",
            "Restaurant Al Riyadh",
            "Restaurant Al Medina",
        ],
    )
    description: str = Field(
        ...,
        title="Описание",
        description="Описание ресторана",
        example="Restaurant Al Faisal is a 5-star restaurant located in the heart of Riyadh, Saudi Arabia.",
    )
    photoUrl: str = Field(
        ...,
        title="URL фото",
        description="URL фото ресторана",
        example="https://s3.geometria.ru/rahma-test/restaurants/Restaurant_Al_Faisal.png",
    )
    avgScore: float = Field(
        ge=0.0,
        le=5.0,
        title="Средний рейтинг",
        description="Средний рейтинг ресторана",
        example=4.5,
    )
    scoreCount: int = Field(
        ge=0,
        title="Количество оценок",
        description="Количество оценок ресторана",
        example=3200,
    )
    isHaram: bool = Field(
        ...,
        title="Харам ли?",
        description="Подаются ли блюда, являющиеся харамом в ресторане",
        examples=[True, False],
    )
    costLevel: CostLevel = Field(
        ...,
        title="Уровень стоимости",
        description="Уровень стоимости ресторана",
        examples=["low", "medium", "high"],
    )

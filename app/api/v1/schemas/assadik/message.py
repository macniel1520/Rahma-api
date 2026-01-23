from typing import List, Optional

from pydantic import BaseModel, Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.api.v1.schemas.sabil.amal_template_schema import AmalTemplateRead
from app.api.v1.schemas.sabil.hotel_schema import HotelRead
from app.api.v1.schemas.sabil.restaurant_schema import RestaurantRead
from app.db.models.enums import Role


class MessageCreate(BaseModel):
    content: str = Field(
        ...,
        title="Текст сообщения",
        description="Текст сообщения пользователя",
        min_length=1,
        max_length=1000,
        example="Привет, как дела?",
    )


class MessageUI(BaseModel):
    hotels: Optional[List[HotelRead]] = Field(
        None,
        title="Отели",
        description="Найденные отели по маршруту",
    )
    restaurants: Optional[List[RestaurantRead]] = Field(
        None,
        title="Рестораны",
        description="Найденные рестораны по маршруту",
    )
    amal_templates: Optional[List[AmalTemplateRead]] = Field(
        None,
        title="Шаблоны амалов",
        description="Найденные шаблоны амалов по маршруту",
    )


class MessageRead(AttributeMixin, CreatedAtMixin, UUIDMixin):
    content: str = Field(
        ...,
        title="Текст сообщения",
        description="Текст сообщения",
        example="Я ассадик, я могу помочь тебе с твоими вопросами.",
    )
    role: Role = Field(..., title="Роль", description="Роль", example="user")
    ui: Optional[MessageUI] = Field(
        None,
        title="UI данные",
        description="Данные для отображения в интерфейсе приложения",
    )

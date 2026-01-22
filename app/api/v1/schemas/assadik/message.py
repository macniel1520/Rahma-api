from pydantic import BaseModel, Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
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


class MessageRead(AttributeMixin, CreatedAtMixin, UUIDMixin):
    content: str = Field(
        ...,
        title="Текст сообщения",
        description="Текст сообщения",
        example="Я ассадик, я могу помочь тебе с твоими вопросами.",
    )
    role: Role = Field(..., title="Роль", description="Роль", example="user")

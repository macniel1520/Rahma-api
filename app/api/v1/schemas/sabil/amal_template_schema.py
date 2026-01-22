from pydantic import Field

from app.api.v1.schemas.common.attrubute_mixin import AttributeMixin
from app.api.v1.schemas.common.created_at_mixin import CreatedAtMixin
from app.api.v1.schemas.common.uuid_mixin import UUIDMixin
from app.db.models.enums import ReccuringRule


class AmalTemplateRead(AttributeMixin, UUIDMixin, CreatedAtMixin):
    title: str = Field(
        ...,
        title="Название",
        description="Название шаблона",
        examples=[
            "Принять Ихрам в Микат",
            "Посетить Мечеть Аль-Харам",
            "Посетить Мечеть Аль-Акса",
        ],
    )
    reccuringRule: ReccuringRule = Field(
        ...,
        title="Правило повторения",
        description="Правило повторения",
        examples=["daily", "weekly", "monthly", "yearly"],
    )

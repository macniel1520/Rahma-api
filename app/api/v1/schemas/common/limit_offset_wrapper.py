from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class LimitOffsetWrapper(BaseModel, Generic[T]):
    count: int = Field(
        ...,
        ge=0,
        title="Общее количество элементов",
        description="Общее количество элементов в списке",
        example=55,
    )
    items: List[T] = Field(
        ...,
        title="Список элементов",
        description="Список элементов в пагинации",
    )

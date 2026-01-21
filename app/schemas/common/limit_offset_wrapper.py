from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class LimitOffsetWrapper(BaseModel, Generic[T]):
    count: int = Field(..., ge=0, description="Total number of items")
    items: List[T] = Field(..., description="List of items")

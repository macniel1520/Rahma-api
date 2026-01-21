import uuid

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: uuid.UUID

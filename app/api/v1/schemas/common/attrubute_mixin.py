from pydantic import BaseModel


class AttributeMixin(BaseModel):
    class Config:
        from_attributes = True

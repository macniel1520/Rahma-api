from pydantic import BaseModel, ConfigDict


class AttributeMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)

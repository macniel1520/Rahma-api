from pydantic import BaseModel, AnyUrl, Field


class JesAuthResponse(BaseModel):
    token: str = Field(
        ..., title="Token", description="Token of the user", example="1234567890"
    )
    redirect: AnyUrl = Field(
        ...,
        title="Redirect",
        description="Redirect url of the user",
        example="https://example.com",
    )

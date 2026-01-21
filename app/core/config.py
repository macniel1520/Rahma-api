from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseModel):
    s3_endpoint: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str
    s3_secure: bool = False

    @property
    def url(self) -> str:
        return f"https://{self.s3_endpoint}/{self.s3_bucket}"


class Settings(BaseSettings):
    s3: S3Settings

    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

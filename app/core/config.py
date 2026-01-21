from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Settings(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    bucket: str
    secure: bool = False

    @property
    def url(self) -> str:
        return f"https://{self.endpoint}/{self.bucket}"


class DB(BaseModel):
    port: int = 5432
    host: str
    password: str
    user: str
    database: str

    @property
    def root(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}"
        )

    @property
    def uri(self) -> str:
        return f"{self.root}/{self.database}"


class Settings(BaseSettings):
    s3: S3Settings
    db: DB

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

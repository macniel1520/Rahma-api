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
        scheme = "https" if self.secure else "http"
        return f"{scheme}://{self.endpoint}/{self.bucket}"


class AISettings(BaseModel):
    api_key: str
    model: str = "deepseek-chat"


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


class SMTP(BaseModel):
    host: str
    port: int
    username: str
    password: str
    sender_email: str
    use_tls: bool
    start_tls: bool

    # Email sending configuration
    timeout: float = 15.0
    retries: int = 3
    base_backoff: float = 0.6


class JWT(BaseModel):
    secret: str
    lifetime_seconds: int


class RefreshToken(BaseModel):
    lifetime_seconds: int


class UserToken(BaseModel):
    secret: str
    lifetime_seconds: int


class JES(BaseModel):
    base_url: str
    api_key: str
    timeout_seconds: float


class Settings(BaseSettings):
    s3: S3Settings
    db: DB
    smtp: SMTP
    jwt: JWT
    user_token: UserToken
    refresh_token: RefreshToken
    ai: AISettings
    jes: JES

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

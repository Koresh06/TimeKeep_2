from pydantic_settings import BaseSettings, SettingsConfigDict
from src.core.config.base import Settings
from src.core.config.postgres import PostgresSettings
from src.core.config.redis import RedisSettings
from src.core.config.security import SecuritySettings


class AppSettings(BaseSettings):
    app: Settings = Settings()
    db: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()

    model_config = SettingsConfigDict(
        env_file=(".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )


settings = AppSettings()
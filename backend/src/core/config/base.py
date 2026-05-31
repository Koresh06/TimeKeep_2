from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "APP_NAME"
    debug: bool = True
    sentry_dsn: str = ""
    allowed_origins: list[str] = ["http://localhost:5173"]

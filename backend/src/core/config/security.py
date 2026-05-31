from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60

from datetime import timedelta

from src.domain.interfaces.services.jwt import IJWTService


class FakeJWTService(IJWTService):

    async def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        return f"access_token_{data['user_id']}"

    async def create_refresh_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        return f"refresh_token_{data['user_id']}"

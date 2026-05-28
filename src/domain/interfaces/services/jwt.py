from datetime import timedelta
from typing import Protocol

from src.domain.enums.role import Role


class IJWTService(Protocol):
    async def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str: ...

    async def create_refresh_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str: ...

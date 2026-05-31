from datetime import timedelta
from typing import Protocol



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

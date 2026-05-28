from dataclasses import dataclass
from functools import lru_cache

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from src.core.config import settings
from src.core.config.security import SecuritySettings
from src.domain.enums.role import Role


@dataclass(frozen=True)
class UserTokenData:
    user_id: int
    role: Role
    department_id: int
    organization_id: int


class GetCurrentUser:
    def __init__(self, settings: SecuritySettings) -> None:
        self.settings = settings

    async def __call__(
        self,
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login")),
    ) -> UserTokenData:
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=[self.settings.algorithm],
            )
            return UserTokenData(
                user_id=int(payload["user_id"]),
                role=Role(payload["role"]),
                department_id=int(payload["department_id"]),
                organization_id=int(payload["organization_id"]),
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Невалидный токен")
        

@lru_cache
def get_current_user() -> GetCurrentUser:
    return GetCurrentUser(settings.security)
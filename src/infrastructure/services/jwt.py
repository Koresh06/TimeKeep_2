from dataclasses import dataclass
from datetime import timedelta, datetime, timezone

from jose import jwt

from src.core.config.security import SecuritySettings
from src.domain.interfaces.services.jwt import IJWTService


@dataclass
class JWTService(IJWTService):
    settings: SecuritySettings

    async def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.settings.access_token_expire_minutes
            )
        to_encode.update(
            {
                "exp": expire,
                "user_id": str(data["user_id"]),
                "role": data["role"].value,
                "department_id": str(data["department_id"]),
                "organization_id": str(data["organization_id"]),
            }
        )
        encoded_jwt = jwt.encode(
            to_encode,
            self.settings.secret_key,
            algorithm=self.settings.algorithm,
        )
        return encoded_jwt

    async def create_refresh_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.settings.refresh_token_expire_minutes
            )
        to_encode.update(
            {
                "exp": expire,
            }
        )
        encoded_jwt = jwt.encode(
            to_encode,
            self.settings.secret_key,
            algorithm=self.settings.algorithm,
        )
        return encoded_jwt

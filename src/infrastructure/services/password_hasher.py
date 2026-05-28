from dataclasses import dataclass
from passlib.context import CryptContext

from src.domain.interfaces.services.password_hasher import IPasswordHasher


@dataclass
class PasswordHasher(IPasswordHasher):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
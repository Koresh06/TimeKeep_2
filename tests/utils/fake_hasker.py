from src.domain.interfaces.services.password_hasher import IPasswordHasher


class FakePasswordHasher(IPasswordHasher):
    async def hash(self, password: str) -> str:
        return password
    
    async def verify(self, password: str, hashed_password: str) -> bool:
        return password == hashed_password
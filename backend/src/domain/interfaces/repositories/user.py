from typing import Protocol

from src.domain.entities.user import User


class IUserRepository(Protocol):
    async def get_by_id(self, id: int) -> User | None: ...

    async def get_by_login(self, login: str) -> User | None: ...

    async def get_all(
        self,
        department_id: int | None = None,
        organization_id: int | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]: ...

    async def create(self, user: User) -> User: ...

    async def update(self, user: User) -> User: ...

    async def delete(self, id: int) -> None: ...

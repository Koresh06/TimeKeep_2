from dataclasses import dataclass, field

from src.domain.entities.user import User
from src.domain.interfaces.repositories.user import IUserRepository
from src.infrastructure.repositories.in_memory.auto_id import _AutoId


@dataclass
class UserInMemoryRepository(IUserRepository):
    _ids: _AutoId = field(default_factory=_AutoId)
    _items: dict[int, User] = field(default_factory=dict)

    async def get_by_id(self, id: int) -> User | None:
        return self._items.get(id)

    async def get_by_login(self, login: str) -> User | None:
        return next(
            (user for user in self._items.values() if user.login == login),
            None,
        )

    async def get_all(
        self,
        department_id: int | None = None,
        organization_id: int | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:
        items = list(self._items.values())

        if department_id is not None:
            items = [d for d in items if d.department_id == department_id]
        if organization_id is not None:
            items = [d for d in items if d.organization_id == organization_id]
        return items[offset : offset + limit]

    async def create(self, user: User) -> User:
        user.id = self._ids.next()
        self._items[user.id] = user
        return user

    async def update(self, user: User) -> User:
        self._items[user.id] = user
        return user

    async def delete(self, id: int) -> None:
        del self._items[id]

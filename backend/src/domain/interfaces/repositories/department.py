from typing import Protocol

from src.domain.entities.department import Department


class IDepartmentRepository(Protocol):
    async def get_by_id(self, id: int) -> Department | None: ...

    async def get_by_name(self, name: str) -> Department | None: ...

    async def create(self, department: Department) -> Department: ...

    async def get_all(
        self,
        organization_id: int | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Department]: ...

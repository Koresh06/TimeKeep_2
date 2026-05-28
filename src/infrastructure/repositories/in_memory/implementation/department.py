from dataclasses import dataclass, field

from src.domain.entities.department import Department
from src.domain.interfaces.repositories.department import IDepartmentRepository
from src.infrastructure.repositories.in_memory.auto_id import _AutoId


@dataclass
class DepartmentInMemoryRepository(IDepartmentRepository):
    _ids: _AutoId = field(default_factory=_AutoId)
    _items: dict[int, Department] = field(default_factory=dict)

    async def get_by_id(self, id: int) -> Department | None:
        return self._items.get(id)

    async def get_by_name(self, name: str) -> Department | None:
        return next(
            (
                department
                for department in self._items.values()
                if department.name == name
            ),
            None,
        )

    async def create(self, department: Department) -> Department:
        department.id = self._ids.next()
        self._items[department.id] = department
        return department

    async def get_all(
        self,
        organization_id: int | None = None,
        offset: int = 0, 
        limit: int = 20,
    ) -> list[Department]:
        items = list(self._items.values())
        if organization_id is not None:
            items = [d for d in items if d.organization_id == organization_id]
        return items[offset:offset + limit]

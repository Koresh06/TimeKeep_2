from dataclasses import dataclass, field
from datetime import date

from src.domain.entities.overtime import Overtime
from src.domain.enums.overtime_status import OvertimeStatus
from src.domain.interfaces.repositories.overtime import IOvertimeRepository
from src.infrastructure.repositories.in_memory.auto_id import _AutoId


@dataclass
class OvertimeInMemoryRepository(IOvertimeRepository):
    _ids: _AutoId = field(default_factory=_AutoId)
    _items: dict[int, Overtime] = field(default_factory=dict)

    async def get_by_id(self, id: int) -> Overtime | None:
        return self._items.get(id)

    async def get_all(
        self,  
        user_id: int | None = None,
        department_id: int | None = None,
        organization_id: int | None = None,
        status: OvertimeStatus | None = None,
        date_: date | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Overtime]:
        items = list(self._items.values())

        if user_id is not None:
            items = [d for d in items if d.user_id == user_id]
        if status is not None:
            items = [d for d in items if d.status == status]
        if date_ is not None:
            items = [d for d in items if d.date_ == date_]
        return items[offset:offset + limit]

    async def create(self, overtime: Overtime) -> Overtime:
        overtime.id = self._ids.next()
        self._items[overtime.id] = overtime
        return overtime

    async def update(self, overtime: Overtime) -> Overtime:
        self._items[overtime.id] = overtime
        return overtime

    async def delete(self, id: int) -> None:
        self._items.pop(id)

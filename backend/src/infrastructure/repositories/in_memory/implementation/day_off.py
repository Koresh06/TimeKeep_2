from dataclasses import dataclass, field
from datetime import date

from src.domain.entities.day_off import DayOff
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.infrastructure.repositories.in_memory.auto_id import _AutoId


@dataclass
class DayOffInMemoryRepository(IDayOffRepository):
    _ids: _AutoId = field(default_factory=_AutoId)
    _items: dict[int, DayOff] = field(default_factory=dict)

    async def get_by_id(self, day_off_id: int) -> DayOff | None:
        return self._items.get(day_off_id)

    async def get_all(
        self,
        user_id: int | None = None,
        department_id: int | None = None,
        organization_id: int | None = None,
        status: DayOffStatus | None = None,
        date_: date | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[DayOff]:
        items = list(self._items.values())

        if user_id is not None:
            items = [d for d in items if d.user_id == user_id]
        if status is not None:
            items = [d for d in items if d.status == status]
        if date_ is not None:
            items = [d for d in items if d.date_ == date_]
        return items[offset : offset + limit]

    async def create(self, day_off: DayOff) -> DayOff:
        day_off.id = self._ids.next()
        self._items[day_off.id] = day_off
        return day_off

    async def update(self, day_off: DayOff) -> DayOff:
        self._items[day_off.id] = day_off
        return day_off

    async def delete(self, id: int) -> None:
        del self._items[id]

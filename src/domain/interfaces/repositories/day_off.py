from datetime import date
from typing import Protocol

from src.domain.entities.day_off import DayOff
from src.domain.enums.day_off_status import DayOffStatus


class IDayOffRepository(Protocol):
    async def get_by_id(self, day_off_id: int) -> DayOff | None: ...

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
        ...

    async def create(self, day_off: DayOff) -> DayOff: ...

    async def update(self, day_off: DayOff) -> DayOff: ...

    async def delete(self, id: int) -> None: ...

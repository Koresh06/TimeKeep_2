from typing import Protocol
from datetime import date

from src.domain.entities.overtime import Overtime
from src.domain.enums.overtime_status import OvertimeStatus


class IOvertimeRepository(Protocol):
    async def get_by_id(self, id: int) -> Overtime | None: ...

    async def get_all(
        self,
        user_id: int | None = None,
        department_id: int | None = None,
        organization_id: int | None = None,
        status: OvertimeStatus | None = None,
        date_: date | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Overtime]: ...

    async def create(self, overtime: Overtime) -> Overtime: ...

    async def update(self, overtime: Overtime) -> Overtime: ...

    async def delete(self, id: int) -> None: ...

from dataclasses import dataclass, field
from datetime import date

from src.domain.entities.base import BaseEntity
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.entities.overtime import Overtime
from src.domain.exceptions.day_off import DayOffAlreadyModeratedError


@dataclass(kw_only=True)
class DayOff(BaseEntity):
    user_id: int
    date_: date
    status: DayOffStatus = field(default=DayOffStatus.PENDING)
    overtimes: list[Overtime]

    def approve(self):
        if self.status != DayOffStatus.PENDING:
            raise DayOffAlreadyModeratedError()
        self.status = DayOffStatus.APPROVED
        self.touch()

    def reject(self):
        if self.status != DayOffStatus.PENDING:
            raise DayOffAlreadyModeratedError()
        self.status = DayOffStatus.REJECTED
        self.touch()

    def format_overtimes_for_document(self) -> str:
        return "; ".join([o.format_for_document() for o in self.overtimes])

from dataclasses import dataclass
from datetime import date, datetime

from src.application.dtos.overtime import OvertimeDTO
from src.domain.entities.day_off import DayOff

from src.domain.enums.day_off_status import DayOffStatus


@dataclass(frozen=True)
class DayOffDTO:
    id: int
    user_id: int
    date_: date
    status: DayOffStatus
    overtimes: list[OvertimeDTO]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: "DayOff") -> "DayOffDTO":
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            date_=entity.date_,
            status=entity.status,
            overtimes=[
                OvertimeDTO.from_entity(o) for o in entity.overtimes
            ],
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

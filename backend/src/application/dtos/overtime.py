from dataclasses import dataclass
from datetime import date, datetime, time

from src.domain.entities.overtime import Overtime
from src.domain.enums.overtime_status import OvertimeStatus


@dataclass(frozen=True)
class OvertimeDTO:
    id: int
    user_id: int
    date_: date
    start_time: time
    end_time: time
    used_hours: float
    description: str
    status: OvertimeStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: "Overtime") -> "OvertimeDTO":
        return cls(
            id=entity.id,
            user_id=entity.user_id,
            date_=entity.date_,
            start_time=entity.start_time,
            end_time=entity.end_time,
            used_hours=entity.used_hours,
            description=entity.description,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

from dataclasses import dataclass, field
from datetime import date, time

from src.domain.entities.base import BaseEntity
from src.domain.enums.overtime_status import OvertimeStatus


@dataclass(kw_only=True)
class Overtime(BaseEntity):
    user_id: int
    date_: date
    start_time: time
    end_time: time
    used_hours: float = 0.0
    description: str
    status: OvertimeStatus = field(default=OvertimeStatus.ACTIVE)

    def duration_hours(self):
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return (end_minutes - start_minutes) / 60

    def available_hours(self):
        return self.duration_hours() - self.used_hours

    def overlaps_with(self, other: "Overtime"):
        if self.date_ != other.date_:
            return False
        return self.start_time < other.end_time and self.end_time > other.start_time

    def mark_as_used(self) -> None:
        if self.available_hours() == 0:
            self.status = OvertimeStatus.USED
            self.touch()

    def format_for_document(self):
        return f"{self.date_.strftime('%d.%m.%Y')} - {self.description} ({self.duration_hours():.0f} ч.)"

from dataclasses import dataclass

from src.domain.entities.overtime import Overtime
from src.domain.enums.work_mode import WorkMode
from src.domain.exceptions.day_off import NotEnoughHoursError


@dataclass(frozen=True)
class WorkSchedule:
    mode: WorkMode

    def required_hours(self):
        if self.mode == WorkMode.DAILY:
            return 8
        return 24

    def select_overtimes_for_dat_off(self, overtimes: list[Overtime]) -> list[Overtime]:
        selected = []
        accumulated_hours = 0
        sort_overtimes = sorted(overtimes, key=lambda o: o.date_)
        for o in sort_overtimes:
            needed = self.required_hours() - accumulated_hours
            if o.available_hours() >= needed:
                o.used_hours += needed
                accumulated_hours += needed
                selected.append(o)
                break
            else:
                hours = o.available_hours()
                o.used_hours += hours
                accumulated_hours += hours
                selected.append(o)
        if accumulated_hours < self.required_hours():
            raise NotEnoughHoursError(
                self.required_hours(),
                accumulated_hours,
            )
        return selected

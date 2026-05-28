from enum import StrEnum


class WorkMode(StrEnum):
    DAILY = "daily"    # ежедневник — нужно 8 часов для отгула
    SHIFT = "shift"    # трёхсменник — нужно 24 часа для отгула
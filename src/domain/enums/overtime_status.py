from enum import StrEnum


class OvertimeStatus(StrEnum):
    ACTIVE = "active"  # не списана, доступна для отгула
    USED = "used"  # списана в счёт отгула

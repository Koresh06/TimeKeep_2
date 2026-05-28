from enum import StrEnum


class DayOffStatus(StrEnum):
    PENDING = "pending"      # ожидает решения модератора
    APPROVED = "approved"    # подтверждён — доступен рапорт
    REJECTED = "rejected"    # отклонён

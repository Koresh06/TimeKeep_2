from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime

from src.utils.get_datetime_utc_now import get_datetime_utc_now


@dataclass(kw_only=True)
class BaseEntity(ABC):
    id: int = field(default=0)
    created_at: datetime = field(default_factory=get_datetime_utc_now)
    updated_at: datetime = field(default_factory=get_datetime_utc_now)

    def touch(self) -> None:
        self.updated_at = get_datetime_utc_now()

    @property
    def is_persisted(self) -> bool:
        return self.id != 0
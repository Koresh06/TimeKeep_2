from dataclasses import dataclass

from src.domain.entities.base import BaseEntity


@dataclass(kw_only=True)
class Organization(BaseEntity):
    name: str
    name_genitive: str
    boss_id: int | None = None
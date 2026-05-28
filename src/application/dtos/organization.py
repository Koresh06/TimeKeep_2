from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.organization import Organization


@dataclass(frozen=True)
class OrganizationDTO:
    id: int
    name: str
    boss_id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: "Organization") -> "OrganizationDTO":
        return cls(
            id=entity.id,
            name=entity.name,
            boss_id=entity.boss_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.department import Department


@dataclass(frozen=True)
class DepartmentDTO:
    id: int
    name: str
    organization_id: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: "Department") -> "DepartmentDTO":
        return cls(
            id=entity.id,
            name=entity.name,
            organization_id=entity.organization_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
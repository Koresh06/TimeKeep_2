from dataclasses import dataclass

from src.domain.entities.base import BaseEntity


@dataclass(kw_only=True)
class Department(BaseEntity):
    name: str
    organization_id: int

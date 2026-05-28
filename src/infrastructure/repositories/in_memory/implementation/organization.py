from dataclasses import dataclass, field

from src.domain.entities.organization import Organization
from src.domain.interfaces.repositories.organization import IOrganizationRepository
from src.infrastructure.repositories.in_memory.auto_id import _AutoId


@dataclass
class OrganizationInMemoryRepository(IOrganizationRepository):
    _ids: _AutoId = field(default_factory=_AutoId)
    _items: dict[int, Organization] = field(default_factory=dict)

    async def get_by_id(self, organization_id: int) -> Organization | None:
        return self._items.get(organization_id)

    async def get_by_name(self, name: str) -> Organization | None:
        return next(
            (
                organization
                for organization in self._items.values()
                if organization.name == name
            ),
            None,
        )

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Organization]:
        return list(self._items.values())[offset : offset + limit]

    async def create(self, organization: Organization) -> Organization:
        organization.id = self._ids.next()
        self._items[organization.id] = organization
        return organization

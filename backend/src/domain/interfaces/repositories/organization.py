from typing import Protocol

from src.domain.entities.organization import Organization


class IOrganizationRepository(Protocol):
    async def get_by_id(self, organization_id: int) -> Organization | None: ...

    async def get_by_name(self, name: str) -> Organization | None: ...

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Organization]: ...

    async def create(self, organization: Organization) -> Organization: ...

    async def update(self, organization: Organization) -> Organization: ...

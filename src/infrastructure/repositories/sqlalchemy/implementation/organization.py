from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities.organization import Organization
from src.domain.interfaces.repositories.organization import IOrganizationRepository
from src.infrastructure.database.models import OrganizationModel


class OrganizationSQLAlchemyRepository(IOrganizationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, organization_id: int) -> Organization | None:
        query = select(OrganizationModel).where(OrganizationModel.id == organization_id)
        result = await self._session.execute(query)
        organization_model = result.scalar_one_or_none()
        return organization_model.to_entity() if organization_model else None

    async def get_by_name(self, name: str) -> Organization | None:
        query = select(OrganizationModel).where(OrganizationModel.name == name)
        result = await self._session.execute(query)
        organization_model = result.scalar_one_or_none()
        return organization_model.to_entity() if organization_model else None

    async def get_all(
        self,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Organization]:
        query = select(OrganizationModel)
        query = query.offset(offset).limit(limit)
        result = await self._session.execute(query)
        return [
            organization_model.to_entity()
            for organization_model in result.scalars().all()
        ]

    async def create(self, organization: Organization) -> Organization:
        organization_model = OrganizationModel.from_entity(organization)
        self._session.add(organization_model)
        await self._session.flush()
        return organization_model.to_entity()

    async def update(self, organization: Organization) -> Organization:
        organization_model = OrganizationModel.from_entity(organization)
        await self._session.merge(organization_model)
        await self._session.flush()
        return organization_model.to_entity()
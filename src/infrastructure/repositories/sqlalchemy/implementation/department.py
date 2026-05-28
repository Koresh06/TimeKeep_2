from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities.department import Department
from src.domain.interfaces.repositories.department import IDepartmentRepository
from src.infrastructure.database.models import DepartmentModel


class DepartmentSQLAlchemyRepository(IDepartmentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: int) -> Department | None:
        query = select(DepartmentModel).where(DepartmentModel.id == id)
        result = await self._session.execute(query)
        department_model = result.scalar_one_or_none()
        return department_model.to_entity() if department_model else None

    async def get_by_name(self, name: str) -> Department | None:
        query = select(DepartmentModel).where(DepartmentModel.name == name)
        result = await self._session.execute(query)
        department_model = result.scalar_one_or_none()
        return department_model.to_entity() if department_model else None

    async def create(self, department: Department) -> Department:
        department_model = DepartmentModel.from_entity(department)
        self._session.add(department_model)
        await self._session.flush()
        return department_model.to_entity()

    async def get_all(
        self,
        organization_id: int | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Department]:
        query = select(DepartmentModel)
        if organization_id:
            query = query.where(DepartmentModel.organization_id == organization_id)
        query = query.offset(offset).limit(limit)
        result = await self._session.execute(query)
        return [
            department_model.to_entity() 
            for department_model in result.scalars().all()
        ]
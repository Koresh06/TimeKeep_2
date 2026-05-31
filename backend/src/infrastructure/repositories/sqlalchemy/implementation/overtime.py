from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities.overtime import Overtime
from src.domain.enums.overtime_status import OvertimeStatus
from src.domain.interfaces.repositories.overtime import IOvertimeRepository
from src.infrastructure.database.models import OvertimeModel
from src.infrastructure.database.models.user import UserModel


class OvertimeSQLAlchemyRepository(IOvertimeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: int) -> Overtime | None:
        query = select(OvertimeModel).where(OvertimeModel.id == id)
        result = await self._session.execute(query)
        overtime_model = result.scalar_one_or_none()
        return overtime_model.to_entity() if overtime_model else None

    async def get_all(
        self,
        user_id: int | None = None,
        department_id: int | None = None,
        organization_id: int | None = None,
        status: OvertimeStatus | None = None,
        date_: date | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Overtime]:
        query = select(OvertimeModel)
        if user_id:
            query = query.where(OvertimeModel.user_id == user_id)
        if status:
            query = query.where(OvertimeModel.status == status)
        if department_id:
            query = query.join(UserModel).where(
                UserModel.department_id == department_id
            )
        if organization_id:
            query = query.join(UserModel).where(
                UserModel.organization_id == organization_id
            )
        if date_:
            query = query.where(OvertimeModel.date_ == date_)
        query = query.offset(offset).limit(limit)
        result = await self._session.execute(query)
        return [overtime_model.to_entity() for overtime_model in result.scalars().all()]

    async def create(self, overtime: Overtime) -> Overtime:
        overtime_model = OvertimeModel.from_entity(overtime)
        self._session.add(overtime_model)
        await self._session.flush()
        return overtime_model.to_entity()

    async def update(self, overtime: Overtime) -> Overtime:
        overtime_model = OvertimeModel.from_entity(overtime)
        await self._session.merge(overtime_model)
        await self._session.flush()
        return overtime_model.to_entity()

    async def delete(self, id: int) -> None:
        query = select(OvertimeModel).where(OvertimeModel.id == id)
        result = await self._session.execute(query)
        overtime_model = result.scalar_one_or_none()
        if overtime_model:
            await self._session.delete(overtime_model)

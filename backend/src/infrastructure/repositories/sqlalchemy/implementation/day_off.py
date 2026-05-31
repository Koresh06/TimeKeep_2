from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.domain.entities.day_off import DayOff
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.infrastructure.database.models import DayOffModel
from src.infrastructure.database.models.day_off_overtime import DayOffOvertimeModel
from src.infrastructure.database.models.user import UserModel


class DayOffSQLAlchemyRepository(IDayOffRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, day_off_id: int) -> DayOff | None:
        result = await self._session.execute(
            select(DayOffModel)
            .where(DayOffModel.id == day_off_id)
            .options(
                selectinload(DayOffModel.day_off_overtimes).selectinload(
                    DayOffOvertimeModel.overtime
                )
            )
        )
        day_off_model = result.scalar_one_or_none()
        return day_off_model.to_entity() if day_off_model else None

    async def get_all(
        self,
        user_id: int | None = None,
        department_id: int | None = None,
        organization_id: int | None = None,
        status: DayOffStatus | None = None,
        date_: date | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[DayOff]:
        query = select(DayOffModel).options(
            selectinload(DayOffModel.day_off_overtimes).selectinload(
                DayOffOvertimeModel.overtime
            )
        )
        if user_id:
            query = query.where(DayOffModel.user_id == user_id)
        if status:
            query = query.where(DayOffModel.status == status)
        if department_id:
            query = query.join(UserModel).where(
                UserModel.department_id == department_id
            )
        if organization_id:
            query = query.join(UserModel).where(
                UserModel.organization_id == organization_id
            )
        if date_:
            query = query.where(DayOffModel.date_ == date_)
        query = query.offset(offset).limit(limit)
        result = await self._session.execute(query)
        return [day_off_model.to_entity() for day_off_model in result.scalars().all()]

    async def create(self, day_off: DayOff) -> DayOff:
        day_off_model = DayOffModel.from_entity(day_off)
        self._session.add(day_off_model)
        await self._session.flush()  # получаем id

        # создаём связи с overtime'ами
        for overtime in day_off.overtimes:
            link = DayOffOvertimeModel(
                day_off_id=day_off_model.id,
                overtime_id=overtime.id,
                used_hours=overtime.used_hours,
            )
            self._session.add(link)

        await self._session.flush()

        # перезагружаем с relationships
        result = await self._session.execute(
            select(DayOffModel)
            .where(DayOffModel.id == day_off_model.id)
            .options(
                selectinload(DayOffModel.day_off_overtimes).selectinload(
                    DayOffOvertimeModel.overtime
                )
            )
        )
        return result.scalar_one().to_entity()

    async def update(self, day_off: DayOff) -> DayOff:
        day_off_model = DayOffModel.from_entity(day_off)
        await self._session.merge(day_off_model)
        await self._session.flush()
        return day_off_model.to_entity()

    async def delete(self, id: int) -> None:
        query = select(DayOffModel).where(DayOffModel.id == id)
        result = await self._session.execute(query)
        day_off_model = result.scalar_one_or_none()
        if day_off_model:
            await self._session.delete(day_off_model)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.domain.entities.user import User
from src.domain.interfaces.repositories.user import IUserRepository
from src.infrastructure.database.models import UserModel


class UserSQLAlchemyRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id: int) -> User | None:
        query = select(UserModel).where(UserModel.id == id)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def get_by_login(self, login: str) -> User | None:
        query = select(UserModel).where(UserModel.login == login)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def get_all(
        self,
        department_id: int | None = None,
        organization_id: int | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[User]:
        query = select(UserModel)
        if department_id:
            query = query.where(UserModel.department_id == department_id)
        if organization_id:
            query = query.where(UserModel.organization_id == organization_id)
        query = query.offset(offset).limit(limit)
        result = await self._session.execute(query)
        return [user_model.to_entity() for user_model in result.scalars().all()]

    async def create(self, user: User) -> User:
        user_model = UserModel.from_entity(user)
        self._session.add(user_model)
        await self._session.flush()
        return user_model.to_entity()

    async def update(self, user: User) -> User:
        user_model = UserModel.from_entity(user)
        await self._session.merge(user_model)
        await self._session.flush()
        return user_model.to_entity()

    async def delete(self, id: int) -> None:
        query = select(UserModel).where(UserModel.id == id)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        if user_model:
            await self._session.delete(user_model)

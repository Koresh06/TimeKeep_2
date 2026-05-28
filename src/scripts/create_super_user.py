import asyncio
import getpass

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings
from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode
from src.domain.entities.user import User
from src.domain.entities.department import Department
from src.domain.entities.organization import Organization
from src.infrastructure.repositories.sqlalchemy.implementation.organization import (
    OrganizationSQLAlchemyRepository,
)
from src.infrastructure.repositories.sqlalchemy.implementation.department import (
    DepartmentSQLAlchemyRepository,
)
from src.infrastructure.repositories.sqlalchemy.implementation.user import (
    UserSQLAlchemyRepository,
)
from src.infrastructure.services.password_hasher import PasswordHasher


async def create_super_user() -> None:
    login = input("Введите логин: ")
    password = getpass.getpass("Введите пароль: ")
    confirm = getpass.getpass("Подтвердите пароль: ")

    if password != confirm:
        print("Пароли не совпадают")
        return

    engine = create_async_engine(settings.db.url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        user_repo = UserSQLAlchemyRepository(session)
        existing = await user_repo.get_by_login(login)
        if existing:
            print(f"Пользователь с логином '{login}' уже существует")
            return

        hasher = PasswordHasher()

        org_repo = OrganizationSQLAlchemyRepository(session)
        org = await org_repo.create(
            Organization(
                name="Главная организация",
                boss_id=1,
            )
        )

        dept_repo = DepartmentSQLAlchemyRepository(session)
        dept = await dept_repo.create(
            Department(
                name="Главный департамент",
                organization_id=org.id,
            )
        )

        user = User.create(
            login=login,
            hashed_password=await hasher.hash(password),
            surname="",
            first_name="",
            patronymic="",
            position="Системный администратор",
            rank=Rank.PRIVATE,
            role=Role.SUPER_ADMIN,
            work_mode=WorkMode.DAILY,
            department_id=dept.id,
            organization_id=org.id,
        )
        await user_repo.create(user)
        await session.commit()
        print(f"Суперюзер с логином '{login}' успешно создан")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_super_user())

from dishka import Scope, provide, Provider
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from src.core.config.postgres import PostgresSettings
from src.core.config.security import SecuritySettings
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.domain.interfaces.repositories.department import IDepartmentRepository
from src.domain.interfaces.repositories.organization import IOrganizationRepository
from src.domain.interfaces.repositories.overtime import IOvertimeRepository
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.services.document_generator import IDocumentGenerator
from src.domain.interfaces.services.jwt import IJWTService
from src.domain.interfaces.services.password_hasher import IPasswordHasher
from src.domain.interfaces.transaction_manager import ITransactionManager
from src.infrastructure.repositories.sqlalchemy.implementation.user import (
    UserSQLAlchemyRepository,
)
from src.infrastructure.repositories.sqlalchemy.implementation.department import (
    DepartmentSQLAlchemyRepository,
)
from src.infrastructure.repositories.sqlalchemy.implementation.organization import (
    OrganizationSQLAlchemyRepository,
)
from src.infrastructure.repositories.sqlalchemy.implementation.overtime import (
    OvertimeSQLAlchemyRepository,
)
from src.infrastructure.repositories.sqlalchemy.implementation.day_off import (
    DayOffSQLAlchemyRepository,
)
from src.infrastructure.repositories.sqlalchemy.transaction_manager import (
    SQLAlchemyTransactionManager,
)
from src.infrastructure.services.document_generator import DocumentGenerator
from src.infrastructure.services.password_hasher import PasswordHasher
from src.infrastructure.services.jwt import JWTService


class InfrastructureProvider(Provider):

    @provide(scope=Scope.APP)
    def get_engine(self, db: PostgresSettings) -> AsyncEngine:
        return create_async_engine(db.url)

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        factory: async_sessionmaker,
    ) -> AsyncGenerator[AsyncSession, None]:
        async with factory() as session:
            yield session

    # repositories
    user_repo = provide(
        UserSQLAlchemyRepository,
        scope=Scope.REQUEST,
        provides=IUserRepository,
    )
    overtime_repo = provide(
        OvertimeSQLAlchemyRepository,
        scope=Scope.REQUEST,
        provides=IOvertimeRepository,
    )
    day_off_repo = provide(
        DayOffSQLAlchemyRepository,
        scope=Scope.REQUEST,
        provides=IDayOffRepository,
    )
    department_repo = provide(
        DepartmentSQLAlchemyRepository,
        scope=Scope.REQUEST,
        provides=IDepartmentRepository,
    )
    organization_repo = provide(
        OrganizationSQLAlchemyRepository,
        scope=Scope.REQUEST,
        provides=IOrganizationRepository,
    )

    # transaction manager
    transaction_manager = provide(
        SQLAlchemyTransactionManager,
        scope=Scope.REQUEST,
        provides=ITransactionManager,
    )
    

    # services
    @provide(scope=Scope.APP, provides=IPasswordHasher)
    def get_password_hasher(self) -> IPasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.APP, provides=IJWTService)
    def get_jwt_service(self, settings: SecuritySettings) -> IJWTService:
        return JWTService(settings)

    @provide(scope=Scope.APP, provides=IDocumentGenerator)
    def get_document_generator(self) -> IDocumentGenerator:
        return DocumentGenerator()
from dataclasses import dataclass

from src.application.dtos.document import DocumentDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.day_off import DayOff
from src.domain.entities.organization import Organization
from src.domain.entities.user import User
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.enums.role import Role
from src.domain.exceptions.day_off import (
    DayOffAccessDeniedError,
    DayOffNotApprovedError,
    DayOffNotFoundError,
)
from src.domain.exceptions.department import DepartmentNotFoundError
from src.domain.exceptions.organization import OrganizationNotFoundError
from src.domain.exceptions.user import UserNotFoundError
from src.domain.interfaces.repositories.department import IDepartmentRepository
from src.domain.interfaces.services.document_generator import IDocumentGenerator
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.domain.interfaces.repositories.organization import IOrganizationRepository
from src.domain.interfaces.repositories.user import IUserRepository


@dataclass(frozen=True, eq=False)
class GenerateReportCommand(UseCaseRequest):
    user_id: int
    day_off_id: int


@dataclass(kw_only=True)
class GenerateReportUseCase(UseCase[GenerateReportCommand, bytes]):
    day_off_repo: IDayOffRepository
    user_repo: IUserRepository
    deprtment_repo: IDepartmentRepository
    organization_repo: IOrganizationRepository
    doc_generator: IDocumentGenerator

    async def __call__(self, command: GenerateReportCommand) -> bytes:
        user: User | None = await self.user_repo.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError(command.user_id)

        day_off: DayOff | None = await self.day_off_repo.get_by_id(command.day_off_id)
        if not day_off:
            raise DayOffNotFoundError(command.day_off_id)

        if day_off.user_id != command.user_id and user.role != Role.SUPER_ADMIN:
            raise DayOffAccessDeniedError()

        if day_off.status != DayOffStatus.APPROVED:
            raise DayOffNotApprovedError()

        organization: Organization | None = await self.organization_repo.get_by_id(
            user.organization_id
        )
        if not organization:
            raise OrganizationNotFoundError(user.organization_id)

        boss = await self.user_repo.get_by_id(organization.boss_id)
        if not boss:
            raise UserNotFoundError(organization.boss_id)

        department = await self.deprtment_repo.get_by_id(user.department_id)
        if not department:
            raise DepartmentNotFoundError(user.department_id)

        report_dto = DocumentDTO.build(day_off, user, organization, boss, department)
        return await self.doc_generator.generate_day_off_document(report_dto)

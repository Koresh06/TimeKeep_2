from dataclasses import dataclass

from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.day_off import DayOff
from src.domain.entities.organization import Organization
from src.domain.entities.user import User
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.exceptions.day_off import DayOffAccessDeniedError, DayOffNotApprovedError, DayOffNotFoundError
from src.domain.exceptions.organization import OrganizationNotFoundError
from src.domain.exceptions.user import UserNotFoundError
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
    organization_repo: IOrganizationRepository
    doc_generator: IDocumentGenerator


    async def __call__(self, command: GenerateReportCommand) -> bytes:
        day_off: DayOff | None = await self.day_off_repo.get_by_id(command.day_off_id)
        if not day_off:
            raise DayOffNotFoundError(command.day_off_id)
        
        if day_off.user_id != command.user_id:
            raise DayOffAccessDeniedError()
        
        if day_off.status != DayOffStatus.APPROVED:
            raise DayOffNotApprovedError()
        
        user: User | None = await self.user_repo.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError(command.user_id)
        
        organization: Organization | None = await self.organization_repo.get_by_id(user.organization_id)
        if not organization:
            raise OrganizationNotFoundError(user.organization_id)
        
        boss = await self.user_repo.get_by_id(organization.boss_id)
        if not boss:
            raise UserNotFoundError(organization.boss_id)

        return await self.doc_generator.generate_day_off_document(
            day_off,
            user,
            organization,
            boss,
        ) 
        
        


from dataclasses import dataclass

from src.application.dtos.organization import OrganizationDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.organization import Organization
from src.domain.exceptions.organization import OrganizationAlreadyExistsError
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.repositories.organization import IOrganizationRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class CreateOrganizationCommand(UseCaseRequest):
    name: str
    name_genitive: str
    boss_id: int


@dataclass(kw_only=True)
class CreateOrganizationUseCase(UseCase[CreateOrganizationCommand, OrganizationDTO]):
    organization_repo: IOrganizationRepository
    transaction_manager: ITransactionManager
    cache: ICache

    async def __call__(self, command: CreateOrganizationCommand) -> OrganizationDTO:
        organization_by_name = await self.organization_repo.get_by_name(command.name)
        if organization_by_name:
            raise OrganizationAlreadyExistsError(command.name)

        organization = Organization(
            name=command.name,
            name_genitive=command.name_genitive,
            boss_id=command.boss_id,
        )
        result = await self.organization_repo.create(organization)
        await self.transaction_manager.commit()

        await self.cache.delete("organizations:offset:0:limit:20")

        return OrganizationDTO.from_entity(result)


    
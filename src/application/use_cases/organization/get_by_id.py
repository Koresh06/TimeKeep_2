from dataclasses import dataclass

from src.application.dtos.organization import OrganizationDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.organization import Organization
from src.domain.exceptions.organization import OrganizationNotFoundError
from src.domain.interfaces.repositories.organization import IOrganizationRepository

@dataclass(frozen=True, eq=False)
class GetOrganizationQuery(UseCaseRequest):
    id: int


@dataclass(kw_only=True)
class GetOrganizationUseCase(UseCase[GetOrganizationQuery, OrganizationDTO]):
    organization_repo: IOrganizationRepository

    async def __call__(self, command: GetOrganizationQuery) -> OrganizationDTO:
        result: Organization | None = await self.organization_repo.get_by_id(command.id)
        if not result:
            raise OrganizationNotFoundError(command.id)

        return OrganizationDTO.from_entity(result)
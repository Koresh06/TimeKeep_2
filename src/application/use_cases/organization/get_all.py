from dataclasses import dataclass

from src.application.dtos.organization import OrganizationDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.organization import Organization
from src.domain.interfaces.repositories.organization import IOrganizationRepository


@dataclass(frozen=True, eq=False)
class GetAllOrganizationQuery(UseCaseRequest):
    offset: int
    limit: int


@dataclass(kw_only=True)
class GetAllOrganizationUseCase(UseCase[GetAllOrganizationQuery, list[OrganizationDTO]]):
    organization_repo: IOrganizationRepository

    async def __call__(self, command: GetAllOrganizationQuery) -> list[OrganizationDTO]:
        result: list[Organization] = await self.organization_repo.get_all(
            offset=command.offset,
            limit=command.limit,
        )
        return [OrganizationDTO.from_entity(department) for department in result]
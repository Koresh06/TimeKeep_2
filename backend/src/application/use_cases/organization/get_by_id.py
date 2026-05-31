from dataclasses import dataclass

from src.application.dtos.organization import OrganizationDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.exceptions.organization import OrganizationNotFoundError
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.repositories.organization import IOrganizationRepository


@dataclass(frozen=True, eq=False)
class GetOrganizationQuery(UseCaseRequest):
    id: int


@dataclass(kw_only=True)
class GetOrganizationUseCase(UseCase[GetOrganizationQuery, OrganizationDTO]):
    organization_repo: IOrganizationRepository
    cache: ICache

    async def __call__(self, command: GetOrganizationQuery) -> OrganizationDTO:
        cache_key = f"organization:{command.id}"

        cached = await self.cache.get(cache_key)
        if cached:
            return OrganizationDTO(**cached)

        result = await self.organization_repo.get_by_id(command.id)
        if not result:
            raise OrganizationNotFoundError(command.id)

        dto = OrganizationDTO.from_entity(result)
        await self.cache.set(cache_key, dto.__dict__, ttl=600)
        return dto

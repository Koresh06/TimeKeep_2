from dataclasses import dataclass

from src.application.dtos.organization import OrganizationDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.organization import Organization
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.repositories.organization import IOrganizationRepository


@dataclass(frozen=True, eq=False)
class GetAllOrganizationQuery(UseCaseRequest):
    offset: int
    limit: int


@dataclass(kw_only=True)
class GetAllOrganizationUseCase(UseCase[GetAllOrganizationQuery, list[OrganizationDTO]]):
    organization_repo: IOrganizationRepository
    cache: ICache

    async def __call__(self, command: GetAllOrganizationQuery) -> list[OrganizationDTO]:
        cache_key = f"organizations:offset:{command.offset}:limit:{command.limit}"

        cached = await self.cache.get(cache_key)
        if cached:
            return [OrganizationDTO(**o) for o in cached]

        result = await self.organization_repo.get_all(
            offset=command.offset,
            limit=command.limit,
        )
        dtos = [OrganizationDTO.from_entity(o) for o in result]
        await self.cache.set(cache_key, [dto.__dict__ for dto in dtos], ttl=600)
        return dtos
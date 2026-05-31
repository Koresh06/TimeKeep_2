from dataclasses import dataclass

from src.application.dtos.token import TokenDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.exceptions.user import InvalidCredentialsError
from src.domain.interfaces.services.jwt import IJWTService
from src.domain.interfaces.services.password_hasher import IPasswordHasher
from src.domain.interfaces.repositories.user import IUserRepository


@dataclass(frozen=True, eq=False)
class LoginCommand(UseCaseRequest):
    login: str
    password: str


@dataclass(kw_only=True)
class LoginUseCase(UseCase[LoginCommand, TokenDTO]):
    user_repo: IUserRepository
    hashed: IPasswordHasher
    jwt: IJWTService

    async def __call__(self, command: LoginCommand) -> TokenDTO:
        user = await self.user_repo.get_by_login(command.login)
        if not user:
            raise InvalidCredentialsError()
        if not await self.hashed.verify(command.password, user.hashed_password):
            raise InvalidCredentialsError()

        return TokenDTO(
            access_token=await self.jwt.create_access_token(
                data={
                    "user_id": user.id,
                    "role": user.role,
                    "department_id": user.department_id,
                    "organization_id": user.organization_id,
                },
            ),
            refresh_token=await self.jwt.create_refresh_token(
                data={
                    "user_id": user.id,
                },
            ),
        )

from dataclasses import dataclass

from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.overtime import Overtime
from src.domain.enums.overtime_status import OvertimeStatus
from src.domain.exceptions.overtime import (
    AccessDeniedError,
    OvertimeAlreadyUsedError,
    OvertimeNotFoundError,
)
from src.domain.interfaces.repositories.overtime import IOvertimeRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class DeleteOvertimeRequest(UseCaseRequest):
    id: int
    user_id: int


@dataclass(kw_only=True)
class DeleteOvertimeUseCase(UseCase[DeleteOvertimeRequest, None]):
    overtime_repository: IOvertimeRepository
    transaction_manager: ITransactionManager

    async def __call__(self, request: DeleteOvertimeRequest) -> None:
        overtime: Overtime | None = await self.overtime_repository.get_by_id(request.id)

        if not overtime:
            raise OvertimeNotFoundError(request.id)
        if request.user_id != overtime.user_id:
            raise AccessDeniedError()
        if overtime.status != OvertimeStatus.ACTIVE:
            raise OvertimeAlreadyUsedError()

        await self.overtime_repository.delete(request.id)
        await self.transaction_manager.commit()

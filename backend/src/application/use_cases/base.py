from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class UseCaseInput(ABC):
    pass


class UseCaseRequest(UseCaseInput):
    pass


class UseCaseQuery(UseCaseInput):
    pass


ReqT = TypeVar("ReqT", bound=UseCaseInput)
ResT = TypeVar("ResT")


class UseCase(ABC, Generic[ReqT, ResT]):
    @abstractmethod
    async def __call__(self, command: ReqT) -> ResT:
        raise NotImplementedError

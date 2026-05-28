from src.domain.exceptions.base import TimeKeepError


class OrganizationNotFoundError(TimeKeepError):
    """Организация не найдена"""
    def __init__(self, organization_id: int) -> None:
        super().__init__(f"Организация с id={organization_id} не найдена")


class OrganizationAlreadyExistsError(TimeKeepError):
    """Организация с таким названием уже существует"""
    def __init__(self, name: str) -> None:
        super().__init__(f"Организация с названием - {name} уже существует")
from src.domain.exceptions.base import TimeKeepError


class DepartmentNotFoundError(TimeKeepError):
    """Департамент не найден."""
    def __init__(self, department_id: int) -> None:
        super().__init__(f"Департамент с id={department_id} не найден")


class DepartmentAlreadyExistsError(TimeKeepError):
    """Департамент с таким названием уже существует."""
    def __init__(self, name: str) -> None:
        super().__init__(f"Департамент с названием - {name} уже существует")
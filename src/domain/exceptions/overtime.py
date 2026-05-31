from src.domain.exceptions.base import TimeKeepError


class OvertimeOverlapError(TimeKeepError):
    """Ошибка перекрытия переработки"""

    def __init__(self) -> None:
        super().__init__("Переработка частично совпадает с существующей")


class AccessDeniedError(TimeKeepError):
    """Ошибка доступа"""

    def __init__(self) -> None:
        super().__init__("Доступ запрещен")


class OvertimeAlreadyUsedError(TimeKeepError):
    """Ошибка использования переработки"""

    def __init__(self) -> None:
        super().__init__("Переработка уже использована")


class OvertimeNotFoundError(TimeKeepError):
    """Ошибка поиска переработки"""

    def __init__(self, id: int) -> None:
        super().__init__(f"Переработка с id={id} не найдена")

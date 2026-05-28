from src.domain.exceptions.base import TimeKeepError


class NotEnoughHoursError(TimeKeepError):
    """Недостаточно накопленных часов для отгула."""
    def __init__(self, required: int, available: float) -> None:
        super().__init__(
            f"Недостаточно часов для отгула. "
            f"Требуется: {required} ч., доступно: {available:.1f} ч."
        )


class DayOffNotFoundError(TimeKeepError):
    """Заявка на отгул не найдена."""
    def __init__(self, day_off_id: int) -> None:
        super().__init__(f"Заявка на отгул с id={day_off_id} не найдена.")


class DayOffAlreadyModeratedError(TimeKeepError):
    """Заявка уже была рассмотрена модератором."""
    def __init__(self) -> None:
        super().__init__(
            "Заявка на отгул уже была рассмотрена модератором."
        )


class DayOffNotApprovedError(TimeKeepError):
    """Рапорт доступен только для подтверждённых заявок."""
    def __init__(self) -> None:
        super().__init__(
            "Рапорт можно получить только для подтверждённой заявки."
        )


class DayOffAccessDeniedError(TimeKeepError):
    def __init__(self) -> None:
        super().__init__("Нет доступа к данной заявке на отгул.")
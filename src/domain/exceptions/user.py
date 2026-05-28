from src.domain.exceptions.base import TimeKeepError


class UserAlreadyExistsError(TimeKeepError):
    """Пользователь с таким логином уже существует"""

    def __init__(self, login: str) -> None:
        super().__init__(f"Пользователь с логином - {login} уже существует")

class InvalidCredentialsError(TimeKeepError):
    """Неверные логин или пароль"""
    def __init__(self) -> None:
        super().__init__(f"Неверные логин или пароль")

class UserNotFoundError(TimeKeepError):
    """Пользователь не найден"""
    def __init__(self, user_id: int) -> None:
        super().__init__(f"Пользователь с id={user_id} не найден")

class UserNotModeratorError(TimeKeepError):
    """Пользователь не является модератором"""
    def __init__(self, user_id: int) -> None:
        super().__init__(f"Пользователь с id={user_id} не является модератором")
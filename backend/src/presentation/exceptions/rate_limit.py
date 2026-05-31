class RateLimitExceededException(Exception):
    """Пользователь превысил лимит запросов"""

    def __init__(self):
        super().__init__("Превышен лимит запросов")

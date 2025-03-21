class ConnectionDBException(Exception):
    def __init__(self, message="Не удалось подключиться к базе данных"):
        super().__init__(message)


class AddEventException(ValueError):
    def __init__(self, message="Нет доступных событий для добавления."):
        super().__init__(message)


class UpdateBalanceEventException(ValueError):
    def __init__(self, message="Не удалось обновить баланс событий."):
        super().__init__(message)


class AddNoticeException(ValueError):
    def __init__(self, message="Нет доступных уведомлений для добавления."):
        super().__init__(message)


class AddNoticeTimeException(ValueError):
    def __init__(self, message="Время уведомления должно быть раньше события."):
        super().__init__(message)


class AddEventTimeException(ValueError):
    def __init__(self, message="Время события не может быть в прошлом."):
        super().__init__(message)


class UpdateBalanceNoticeException(ValueError):
    def __init__(self, message="Не удалось обновить баланс уведомлений."):
        super().__init__(message)


class NotCorrectRequestException(ValueError):
    def __init__(self, message="Некорректный запрос"):
        super().__init__(message)


class NoEventException(ValueError):
    def __init__(self, message="Событие не найденно"):
        super().__init__(message)


class NotCorrectFixTimeEventException(ValueError):
    def __init__(self, message="Не корректно изменено время события"):
        super().__init__(message)

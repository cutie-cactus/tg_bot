class ConnectionDBException(Exception):
    """!
    @brief Исключение при проблемах подключения к базе данных
    
    @details Возникает при невозможности установить соединение с СУБД
    """
    def __init__(self, message="Не удалось подключиться к базе данных"):
        super().__init__(message)


class AddEventException(ValueError):
    """!
    @brief Исключение при ошибке добавления события
    
    @details Возникает, когда нет доступных событий для добавления
    """
    def __init__(self, message="Нет доступных событий для добавления."):
        super().__init__(message)


class UpdateBalanceEventException(ValueError):
    """!
    @brief Исключение при ошибке обновления баланса событий
    
    @details Возникает при неудачной попытке обновить счетчик событий
    """
    def __init__(self, message="Не удалось обновить баланс событий."):
        super().__init__(message)


class AddNoticeException(ValueError):
    """!
    @brief Исключение при ошибке добавления уведомления
    
    @details Возникает, когда нет доступных уведомлений для добавления
    """
    def __init__(self, message="Нет доступных уведомлений для добавления."):
        super().__init__(message)


class AddNoticeTimeException(ValueError):
    """!
    @brief Исключение при неверном времени уведомления
    
    @details Возникает, когда время уведомления установлено позже времени события
    """
    def __init__(self, message="Время уведомления должно быть раньше события."):
        super().__init__(message)


class AddEventTimeException(ValueError):
    """!
    @brief Исключение при неверном времени события
    
    @details Возникает, когда время события установлено в прошлом
    """
    def __init__(self, message="Время события не может быть в прошлом."):
        super().__init__(message)


class UpdateBalanceNoticeException(ValueError):
    """!
    @brief Исключение при ошибке обновления баланса уведомлений
    
    @details Возникает при неудачной попытке обновить счетчик уведомлений
    """
    def __init__(self, message="Не удалось обновить баланс уведомлений."):
        super().__init__(message)


class NotCorrectRequestException(ValueError):
    """!
    @brief Исключение при некорректном запросе
    
    @details Возникает при получении запроса с неверными или неполными данными
    """
    def __init__(self, message="Некорректный запрос"):
        super().__init__(message)


class NoEventException(ValueError):
    """!
    @brief Исключение при отсутствии события
    
    @details Возникает, когда запрашиваемое событие не найдено в базе
    """
    def __init__(self, message="Событие не найденно"):
        super().__init__(message)


class NotCorrectFixTimeEventException(ValueError):
    """!
    @brief Исключение при некорректном изменении времени события
    
    @details Возникает при попытке установить недопустимое время для события
    """
    def __init__(self, message="Не корректно изменено время события"):
        super().__init__(message)

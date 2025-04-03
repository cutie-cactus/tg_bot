from abc import ABC, abstractmethod


class UserServiceI(ABC):
    """@interface
    @brief Абстрактный интерфейс сервиса для работы с пользователями
    @details Реализует базовые операции управления пользователями: создание, изменение временной зоны, получение статистики
    """

    @abstractmethod
    def add(self, tg_id: str, chat_id: str):
        """@brief Зарегистрировать нового пользователя
        @param tg_id[in] - Уникальный идентификатор пользователя в Telegram
        @param chat_id[in] - Идентификатор чата для коммуникации
        @throws UserAlreadyExistsException если пользователь уже зарегистрирован
        """
        pass

    @abstractmethod
    def change_time_zone(self, tg_id: str, time_zone: int):
        """@brief Обновить временную зону пользователя
        @param tg_id[in] - Идентификатор пользователя в Telegram
        @param time_zone[in] - Новая временная зона в формате UTC offset
        @throws UserNotFoundException если пользователь не найден
        @throws InvalidValueException если некорректное значение временной зоны
        """
        pass

    @abstractmethod
    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        """@brief Получить количество событий пользователя
        @param tg_id[in] - Идентификатор пользователя в Telegram
        @param chat_id[in] - Идентификатор чата для верификации
        @return Количество событий (0 если отсутствуют)
        @throws UserNotFoundException если пользователь не найден
        """
        pass

    @abstractmethod
    def get_time_zone(self, tg_id: str) -> int:
        """@brief Получить текущую временную зону пользователя
        @param tg_id[in] - Идентификатор пользователя в Telegram
        @return Текущая временная зона в формате UTC offset
        @throws UserNotFoundException если пользователь не найден
        """
        pass

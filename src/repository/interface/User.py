from abc import ABC, abstractmethod


class UserRepositoryI(ABC):
    """@brief Абстрактный интерфейс репозитория пользователей
    
    Определяет базовые операции для управления данными пользователей,
    включая временные зоны и счетчики событий.
    @ingroup RepositoryInterface
    """

    @abstractmethod
    def add(self, tg_id: str, chat_id: str):
        """@brief Создание новой записи пользователя
        
        @param tg_id: Уникальный идентификатор пользователя в Telegram
        @param chat_id: Идентификатор чата для привязки
        @throws AlreadyExistsError если пользователь уже зарегистрирован
        """
        pass

    @abstractmethod
    def change_time_zone(self, tg_id: str, time_zone: int):
        """@brief Обновление временной зоны пользователя
        
        @param tg_id: Уникальный идентификатор пользователя в Telegram
        @param time_zone: Новое значение временной зоны (UTC offset в часах)
        @throws NotFoundError если пользователь не найден
        """
        pass

    @abstractmethod
    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        """@brief Получение количества событий пользователя
        
        @param tg_id: Уникальный идентификатор пользователя в Telegram
        @param chat_id: Идентификатор чата для фильтрации
        @return Количество связанных событий
        @throws NotFoundError если пользователь или чат не найдены
        """
        pass

    @abstractmethod
    def get_time_zone(self, tg_id: str) -> int:
        """@brief Получение временной зоны пользователя
        
        @param tg_id: Уникальный идентификатор пользователя в Telegram
        @return Текущая временная зона (UTC offset в часах)
        @throws NotFoundError если пользователь не найден
        """
        pass

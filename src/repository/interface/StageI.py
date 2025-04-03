from abc import ABC, abstractmethod

from dto.stage import WindowType, StageType


class StageRepositoryI(ABC):
    """@brief Абстрактный интерфейс репозитория управления состоянием пользователя
    
    Определяет методы для работы с текущим этапом, окном, 
    привязанными событиями и уведомлениями пользователя.
    @ingroup RepositoryInterface
    """

    @abstractmethod
    def add(self, user_id: str, window: WindowType, stage: StageType):
        """@brief Создание новой записи состояния пользователя
        
        @param user_id: Уникальный идентификатор пользователя
        @param window: Тип окна для инициализации
        @param stage: Тип этапа для инициализации
        @throws AlreadyExistsError если запись для пользователя уже существует
        """
        pass

    @abstractmethod
    def change_window(self, user_id: str, window: WindowType):
        """@brief Изменение типа окна пользователя
        
        @param user_id: Уникальный идентификатор пользователя
        @param window: Новый тип окна
        @throws NotFoundError если пользователь не найден
        """
        pass

    @abstractmethod
    def change_stage(self, user_id: str, stage: StageType):
        """@brief Изменение типа этапа пользователя
        
        @param user_id: Уникальный идентификатор пользователя
        @param stage: Новый тип этапа
        @throws NotFoundError если пользователь не найден
        """
        pass

    @abstractmethod
    def change_event(self, user_id: str, event_id: int):
        """@brief Привязка события к пользователю
        
        @param user_id: Уникальный идентификатор пользователя
        @param event_id: Идентификатор связанного события
        @throws NotFoundError если пользователь или событие не найдены
        """
        pass

    @abstractmethod
    def change_notice(self, user_id: str, notice_id: int):
        """@brief Привязка уведомления к пользователю
        
        @param user_id: Уникальный идентификатор пользователя
        @param notice_id: Идентификатор связанного уведомления
        @throws NotFoundError если пользователь или уведомление не найдены
        """
        pass

    @abstractmethod
    def get_stage(self, user_id: str) -> StageType:
        """@brief Получение текущего этапа пользователя
        
        @param user_id: Уникальный идентификатор пользователя
        @return Текущий тип этапа
        @throws NotFoundError если запись не найдена
        """
        pass

    @abstractmethod
    def get_window(self, user_id: str) -> WindowType:
        """@brief Получение текущего окна пользователя
        
        @param user_id: Уникальный идентификатор пользователя
        @return Текущий тип окна
        @throws NotFoundError если запись не найдена
        """
        pass

    @abstractmethod
    def get_event(self, user_id: str) -> int:
        """@brief Получение привязанного события
        
        @param user_id: Уникальный идентификатор пользователя
        @return ID события или -1 если не привязано
        @throws NotFoundError если пользователь не найден
        """
        pass

    @abstractmethod
    def get_notice(self, user_id: str) -> int:
        """@brief Получение привязанного уведомления
        
        @param user_id: Уникальный идентификатор пользователя
        @return ID уведомления или -1 если не привязано
        @throws NotFoundError если пользователь не найден
        """
        pass

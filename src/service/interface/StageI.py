from abc import ABC, abstractmethod

from dto.stage import WindowType, StageType


class StageServiceI(ABC):
    """@interface
    @brief Абстрактный интерфейс сервиса для управления состоянием пользователя
    @details Обеспечивает методы для работы с этапами взаимодействия, окнами и привязкой к событиям/уведомлениям
    """

    @abstractmethod
    def add(self, user_id: str):
        """@brief Создать новую запись состояния для пользователя
        @param user_id[in] - Идентификатор пользователя
        @throws UserNotFoundException если пользователь не существует
        """
        pass

    @abstractmethod
    def change_window(self, user_id: str, window: WindowType):
        """@brief Изменить тип активного окна
        @param user_id[in] - Идентификатор пользователя
        @param window[in] - Новый тип окна
        @throws UserNotFoundException если пользователь не найден
        @throws InvalidTypeException если передан некорректный тип окна
        """
        pass

    @abstractmethod
    def change_stage(self, user_id: str, stage: StageType):
        """@brief Изменить этап взаимодействия
        @param user_id[in] - Идентификатор пользователя
        @param stage[in] - Новый этап взаимодействия
        @throws UserNotFoundException если пользователь не найден
        @throws InvalidTypeException если передан некорректный тип этапа
        """
        pass

    @abstractmethod
    def change_event(self, user_id: str, event_id: int):
        """@brief Обновить привязанное событие
        @param user_id[in] - Идентификатор пользователя
        @param event_id[in] - ID связанного события
        @throws EventNotFoundException если событие не существует
        @throws PermissionDeniedException если нет прав на привязку
        """
        pass

    @abstractmethod
    def change_notice(self, user_id: str, notice_id: int):
        """@brief Обновить привязанное уведомление
        @param user_id[in] - Идентификатор пользователя
        @param notice_id[in] - ID связанного уведомления
        @throws NoticeNotFoundException если уведомление не существует
        @throws PermissionDeniedException если нет прав на привязку
        """
        pass

    @abstractmethod
    def get_stage(self, user_id: str) -> StageType:
        """@brief Получить текущий этап взаимодействия
        @param user_id[in] - Идентификатор пользователя
        @return Текущий StageType пользователя
        @throws UserNotFoundException если пользователь не найден
        """
        pass

    @abstractmethod
    def get_window(self, user_id: str) -> WindowType:
        """@brief Получить текущее активное окно
        @param user_id[in] - Идентификатор пользователя
        @return Текущий WindowType пользователя
        @throws UserNotFoundException если пользователь не найден
        """
        pass

    @abstractmethod
    def get_event(self, user_id: str) -> int:
        """@brief Получить ID привязанного события
        @param user_id[in] - Идентификатор пользователя
        @return ID события или 0 если нет привязки
        @throws UserNotFoundException если пользователь не найден
        """
        pass

    @abstractmethod
    def get_notice(self, user_id: str) -> int:
        """@brief Получить ID привязанного уведомления
        @param user_id[in] - Идентификатор пользователя
        @return ID уведомления или 0 если нет привязки
        @throws UserNotFoundException если пользователь не найден
        """
        pass

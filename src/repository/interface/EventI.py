"""!
@file EventRepositoryI.py
@brief Интерфейс репозитория для работы с событиями
"""

from abc import ABC, abstractmethod
import dto.event as eventDTO
import model.event as eventModel


class EventRepositoryI(ABC):
    """!
    @brief Абстрактный интерфейс репозитория событий

    @details Определяет контракт для всех реализаций репозиториев событий.
    Обеспечивает единый интерфейс для работы с событиями независимо от реализации хранилища.
    """

    @abstractmethod
    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
        """!
        @brief Абстрактный метод добавления нового события

        @param add_event_request: DTO с данными для создания события
        @type add_event_request: eventDTO.AddEventRequest

        @return ID созданного события
        @rtype: int
        """
        pass

    @abstractmethod
    def change(self, change_event_request: eventDTO.ChangeEventRequest):
        """!
        @brief Абстрактный метод изменения существующего события

        @param change_event_request: DTO с данными для изменения события
        @type change_event_request: eventDTO.ChangeEventRequest
        """
        pass

    @abstractmethod
    def delete(self, user_id: str, event_id: int):
        """!
        @brief Абстрактный метод удаления события

        @param user_id: Идентификатор пользователя
        @type user_id: str
        @param event_id: Идентификатор события
        @type event_id: int
        """
        pass

    @abstractmethod
    def delete_all(self, user_id: str):
        """!
        @brief Абстрактный метод удаления всех событий пользователя

        @param user_id: Идентификатор пользователя
        @type user_id: str
        """
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> list[eventModel.Event]:
        """!
        @brief Абстрактный метод получения всех событий пользователя

        @param user_id: Идентификатор пользователя
        @type user_id: str

        @return Список событий пользователя
        @rtype: list[eventModel.Event]
        """
        pass

    @abstractmethod
    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        """!
        @brief Абстрактный метод получения конкретного события

        @param event_id: Идентификатор события
        @type event_id: int
        @param user_id: Идентификатор пользователя
        @type user_id: str

        @return Найденное событие или None
        @rtype: eventModel.Event | None
        """
        pass

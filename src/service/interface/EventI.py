from abc import ABC, abstractmethod

import dto.event as eventDTO
import model.event as eventModel


class EventServiceI(ABC):
    """@interface
    @brief Абстрактный интерфейс сервиса для работы с событиями
    @details Определяет базовые методы для управления событиями (добавление, изменение, удаление, получение)
    """

    @abstractmethod
    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
        """@brief Добавить новое событие
        @param add_event_request[in] - DTO объект с данными для создания события
        @return ID созданного события
        """
        pass

    @abstractmethod
    def change(self, change_event_request: eventDTO.ChangeEventRequest):
        """@brief Изменить существующее событие
        @param change_event_request[in] - DTO объект с данными для изменения события
        @throws EventNotFoundException если событие не найдено
        """
        pass

    @abstractmethod
    def delete(self, user_id: str, event_id: int):
        """@brief Удалить конкретное событие
        @param user_id[in] - ID пользователя-владельца
        @param event_id[in] - ID удаляемого события
        @throws EventNotFoundException если событие не найдено
        @throws PermissionDeniedException если пользователь не владелец
        """
        pass

    @abstractmethod
    def delete_all(self, user_id: str):
        """@brief Удалить все события пользователя
        @param user_id[in] - ID пользователя чьи события удаляем
        @throws EmptyRepositoryException если события отсутствуют
        """
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> list[eventModel.Event]:
        """@brief Получить все события пользователя
        @param user_id[in] - ID пользователя
        @return Список объектов Event или пустой список
        """
        pass

    @abstractmethod
    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        """@brief Получить конкретное событие
        @param event_id[in] - ID запрашиваемого события
        @param user_id[in] - ID пользователя
        @return Объект Event
        @throws EventNotFoundException если событие не найдено
        """
        pass

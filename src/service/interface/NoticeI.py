from abc import ABC, abstractmethod

import dto.notice as noticeDTO
import model.notice as noticeModel


class NoticeServiceI(ABC):
    """@interface
    @brief Абстрактный интерфейс сервиса для работы с уведомлениями
    @details Определяет базовые методы для управления уведомлениями (создание, получение, удаление, проверка существования)
    """

    @abstractmethod
    def add(self, add_notice_request: noticeDTO.AddNoticeRequest) -> int:
        """@brief Создать новое уведомление
        @param add_notice_request[in] - DTO объект с данными для создания уведомления
        @return ID созданного уведомления
        @throws InvalidEventException если привязанное событие не существует
        """
        pass

    @abstractmethod
    def get(self, notice_id: int) -> noticeModel.Notice:
        """@brief Получить уведомление по ID
        @param notice_id[in] - ID запрашиваемого уведомления
        @return Объект Notice
        @throws NoticeNotFoundException если уведомление не найдено
        """
        pass

    @abstractmethod
    def get_all(self, event_id: int) -> list[noticeModel.Notice]:
        """@brief Получить все уведомления события
        @param event_id[in] - ID целевого события
        @return Список объектов Notice или пустой список
        @throws EventNotFoundException если событие не существует
        """
        pass

    @abstractmethod
    def delete(self, notice_id: int, event_id: int):
        """@brief Удалить уведомление
        @param notice_id[in] - ID удаляемого уведомления
        @param event_id[in] - ID связанного события
        @throws NoticeNotFoundException если уведомление не найдено
        @throws PermissionDeniedException если уведомление не принадлежит событию
        """
        pass

    @abstractmethod
    def check_exist(self, notice_id: int) -> bool:
        """@brief Проверить существование уведомления
        @param notice_id[in] - ID проверяемого уведомления
        @return True если существует, False в противном случае
        """
        pass

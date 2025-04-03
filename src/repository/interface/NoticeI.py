from abc import ABC, abstractmethod

import dto.notice as noticeDTO
import model.notice as noticeModel


class NoticeRepositoryI(ABC):
    """@brief Абстрактный интерфейс репозитория для работы с уведомлениями
    
    Определяет базовые операции для работы с хранилищем уведомлений.
    @ingroup RepositoryInterface
    """

    @abstractmethod
    def add(self, add_notice_request: noticeDTO.AddNoticeRequest) -> int:
        """@brief Добавление нового уведомления
         
        @param add_notice_request: DTO объект с данными для создания уведомления
        @return ID созданного уведомления
        """
        pass

    @abstractmethod
    def get(self, notice_id: int) -> noticeModel.Notice:
        """@brief Получение уведомления по ID
        
        @param notice_id: Идентификатор запрашиваемого уведомления
        @return Объект уведомления из модели
        @throws NotFoundError если уведомление не найдено
        """
        pass

    @abstractmethod
    def get_all(self, event_id: int) -> list[noticeModel.Notice]:
        """@brief Получение всех уведомлений для события
        
        @param event_id: Идентификатор родительского события
        @return Список объектов уведомлений
        """
        pass

    @abstractmethod
    def delete(self, notice_id: int, event_id: int):
        """@brief Удаление уведомления
        
        @param notice_id: Идентификатор удаляемого уведомления
        @param event_id: Идентификатор родительского события (для проверки принадлежности)
        @throws PermissionError если уведомление не принадлежит указанному событию
        """
        pass

    @abstractmethod
    def check_exist(self, notice_id: int) -> bool:
        """@brief Проверка существования уведомления
        
        @param notice_id: Идентификатор проверяемого уведомления
        @return True если уведомление существует, иначе False
        """
        pass

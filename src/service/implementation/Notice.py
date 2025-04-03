import repository.connector.PGConnector as Connector
import service.interface.NoticeI as noticeService
import repository.interface.NoticeI as noticeStorage

import logger.Logger as Logger

import hashlib

import dto.notice as noticeDTO
import model.notice as noticeModel


class NoticeService(noticeService.NoticeServiceI):
    """@brief Сервис для управления напоминаниями
    
    Обеспечивает бизнес-логику работы с напоминаниями:
    - Валидацию данных
    - Логирование операций
    - Обработку ошибок
    @ingroup NoticeService
    """
    
    def __init__(self, connector: Connector.PostgresDBConnector, notice_storage: noticeStorage.NoticeRepositoryI,
                 logger: Logger.Logger):
        """@brief Инициализация сервиса напоминаний
        
        @param connector: Коннектор к PostgreSQL базе данных
        @param notice_storage: Репозиторий для работы с хранилищем напоминаний
        @param logger: Логгер для записи операций
        """
        self.connector = connector
        self.notice_storage = notice_storage
        self.logger = logger

    @staticmethod
    def hash_id(string: str) -> str:
        """@brief Генерация хеша строки
        
        @param string: Входная строка для хеширования
        @return SHA-256 хеш в виде hex-строки
        """
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    # Дублирующийся метод (вероятно ошибка в коде)
    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, add_notice_request: noticeDTO.AddNoticeRequest) -> int:
        """@brief Добавление нового напоминания
        
        @param add_notice_request: DTO с данными для создания напоминания
        @return ID созданного напоминания
        @throws ValueError При некорректных входных данных
        @throws Exception При ошибках уровня хранилища
        """
        try:
            result = self.notice_storage.add(add_notice_request)
            self.logger.info(f"Успешно добавленно напоминание: event_id: {add_notice_request.event_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при добавлении напоминания: {e}, "
                                f"add_notice_request: {add_notice_request}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении напоминания: {e}, "
                                f"add_notice_request: {add_notice_request}")
            raise e

    def get(self, notice_id: int) -> noticeModel.Notice:
        """@brief Получение напоминания по ID
        
        @param notice_id: Идентификатор запрашиваемого напоминания
        @return Объект напоминания
        @throws ValueError При некорректном ID
        @throws Exception При ошибках уровня хранилища
        """
        try:
            result = self.notice_storage.get(notice_id)
            self.logger.info(f"Успешно получено напоминание: notice_id: {notice_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении напоминания: {e}, notice_id: {notice_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении напоминания: {e}, notice_id: {notice_id}")
            raise e

    def get_all(self, event_id: int) -> list[noticeModel.Notice]:
        """@brief Получение всех напоминаний события
        
        @param event_id: Идентификатор родительского события
        @return Список объектов напоминаний
        @throws ValueError При некорректном event_id
        @throws Exception При ошибках уровня хранилища
        """
        try:
            result = self.notice_storage.get_all(event_id)
            self.logger.info(f"Успешно получены все напоминания: event_id: {event_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении всех напоминаний: {e}, event_id: {event_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении всех напоминаний: {e}, event_id: {event_id}")
            raise e

    def delete(self, notice_id: int, event_id: int):
        """@brief Удаление напоминания
        
        @param notice_id: Идентификатор удаляемого напоминания
        @param event_id: Идентификатор родительского события
        @throws ValueError При некорректных идентификаторах
        @throws Exception При ошибках уровня хранилища
        """
        try:
            self.notice_storage.delete(notice_id, event_id)
            self.logger.info(f"Успешно удалено напоминание: notice_id: {notice_id}, event_id: {event_id}")
        except ValueError as e:
            self.logger.warning(f"Ошибка при удалении напоминания: {e}, notice_id: {notice_id}, event_id: {event_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при удалении напоминания: {e}, notice_id: {notice_id}, event_id: {event_id}")
            raise e

    def check_exist(self, notice_id: int) -> bool:
        """@brief Проверка существования напоминания
        
        @param notice_id: Идентификатор проверяемого напоминания
        @return True если напоминание существует, иначе False
        @throws ValueError При некорректном ID
        @throws Exception При ошибках уровня хранилища
        """
        try:
            result = self.notice_storage.check_exist(notice_id)
            self.logger.info(f"Успешно проверено напоминание: notice_id: {notice_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при проверке напоминания: {e}, notice_id: {notice_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при проверке напоминания: {e}, notice_id: {notice_id}")
            raise e

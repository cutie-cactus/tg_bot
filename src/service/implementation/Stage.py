import repository.connector.PGConnector as Connector
import service.interface.StageI as stageService
import repository.interface.StageI as stageStorage
import logger.Logger as Logger
import hashlib

from dto.stage import WindowType, StageType


class StageService(stageService.StageServiceI):
    """@brief Сервис управления состоянием пользователя
    
    Обрабатывает текущий контекст взаимодействия пользователя с системой:
    - Тип активного окна интерфейса
    - Этап workflow
    - Привязанные сущности (события и напоминания)
    @ingroup StageService
    """
    
    def __init__(self, connector: Connector.PostgresDBConnector, stage_storage: stageStorage.StageRepositoryI,
                 logger: Logger.Logger):
        """@brief Инициализация сервиса состояний
        
        @param connector: Коннектор к PostgreSQL базе данных
        @param stage_storage: Репозиторий для работы с хранилищем состояний
        @param logger: Логгер для записи операций
        """
        self.connector = connector
        self.stage_storage = stage_storage
        self.logger = logger

    @staticmethod
    def hash_id(string: str) -> str:
        """@brief Генерация анонимизированного идентификатора
        
        @param string: Оригинальный user_id из Telegram
        @return SHA-256 хеш в виде hex-строки
        """
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, user_id: str):
        """@brief Создание начального состояния пользователя
        
        Инициализирует состояние с параметрами:
        - WindowType.MAIN_KEYBOARD
        - StageType.NONE
        
        @param user_id: Идентификатор пользователя в Telegram
        @return Результат операции
        @throws ValueError При некорректном user_id
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.add(temp_user_id, WindowType.MAIN_KEYBOARD, StageType.NONE)
            self.logger.info(f"Успешно создано состояние: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при создании состояния: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при создании состояния: {e}, user_id: {temp_user_id}")
            raise e

    def change_window(self, user_id: str, window: WindowType):
        """@brief Изменение типа активного окна
        
        @param user_id: Идентификатор пользователя в Telegram
        @param window: Новый тип окна из перечисления WindowType
        @return Результат операции
        @throws ValueError При некорректных параметрах
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_window(temp_user_id, window)
            self.logger.info(f"Успешно изменено состояние окна: user_id: {temp_user_id}, window: {window}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при изменении состояние окна: {e}, user_id: {temp_user_id}, window: {window}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при изменении состояние окна: {e}, user_id: {temp_user_id}, window: {window}")
            raise e

    def change_stage(self, user_id: str, stage: StageType):
        """@brief Изменение этапа workflow
        
        @param user_id: Идентификатор пользователя в Telegram
        @param stage: Новый этап из перечисления StageType
        @return Результат операции
        @throws ValueError При некорректных параметрах
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_stage(temp_user_id, stage)
            self.logger.info(f"Успешно изменено состояние ожидания: user_id: {temp_user_id}, stage: {stage}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при изменении состояние ожидания: {e}, user_id: {temp_user_id}, stage: {stage}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при изменении состояние ожидания: {e}, user_id: {temp_user_id}, stage: {stage}")
            raise e

    def change_event(self, user_id: str, event_id: int):
        """@brief Привязка текущего события
        
        @param user_id: Идентификатор пользователя в Telegram
        @param event_id: ID связываемого события
        @return Результат операции
        @throws ValueError При некорректных параметрах
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_event(temp_user_id, event_id)
            self.logger.info(f"Успешно изменено выбранное событие: user_id: {temp_user_id}, event_id: {event_id}")
            return result
        except ValueError as e:
            self.logger.warning(
                f"Ошибка при изменении выбранного событие: {e}, user_id: {temp_user_id}, event_id: {event_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при изменении выбранного событие: {e}, user_id: {temp_user_id}, event_id: {event_id}")
            raise e

    def change_notice(self, user_id: str, notice_id: int):
        """@brief Привязка текущего напоминания
        
        @param user_id: Идентификатор пользователя в Telegram
        @param notice_id: ID связываемого напоминания
        @return Результат операции
        @throws ValueError При некорректных параметрах
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_notice(temp_user_id, notice_id)
            self.logger.info(f"Успешно изменено выбранное напоминание: user_id: {temp_user_id}, notice_id: {notice_id}")
            return result
        except ValueError as e:
            self.logger.warning(
                f"Ошибка при изменении выбранного напоминания: {e}, user_id: {temp_user_id}, notice_id: {notice_id}")
            raise e
        except Exception as e:
            self.logger.error(
                f"Ошибка при изменении выбранного напоминания: {e}, user_id: {temp_user_id}, notice_id: {notice_id}")
            raise e

    def get_stage(self, user_id: str) -> StageType:
        """@brief Получение текущего этапа workflow
        
        @param user_id: Идентификатор пользователя в Telegram
        @return Текущий этап из перечисления StageType
        @throws ValueError При некорректном user_id
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_stage(temp_user_id)
            self.logger.info(f"Успешно получено состояние ожидания: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении состояния ожидания: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении состояния ожидания: {e}, user_id: {temp_user_id}")
            raise e

    def get_window(self, user_id: str) -> WindowType:
        """@brief Получение текущего окна интерфейса
        
        @param user_id: Идентификатор пользователя в Telegram
        @return Текущий тип окна из перечисления WindowType
        @throws ValueError При некорректном user_id
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_window(temp_user_id)
            self.logger.info(f"Успешно получено состояние окна: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении состояния окна: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении состояния окна: {e}, user_id: {temp_user_id}")
            raise e

    def get_event(self, user_id: str) -> int:
        """@brief Получение привязанного события
        
        @param user_id: Идентификатор пользователя в Telegram
        @return ID привязанного события или -1 если отсутствует
        @throws ValueError При некорректном user_id
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_event(temp_user_id)
            self.logger.info(f"Успешно получено выбранное событие: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении выбранного события: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении выбранного события: {e}, user_id: {temp_user_id}")
            raise e

    def get_notice(self, user_id: str) -> int:
        """@brief Получение привязанного напоминания
        
        @param user_id: Идентификатор пользователя в Telegram
        @return ID привязанного напоминания или -1 если отсутствует
        @throws ValueError При некорректном user_id
        @throws Exception При ошибках уровня хранилища
        """
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_notice(temp_user_id)
            self.logger.info(f"Успешно получено выбранное напоминание: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении выбранного напоминания: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении выбранного напоминания: {e}, user_id: {temp_user_id}")
            raise e

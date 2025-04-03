import repository.interface.User as userRepository
import service.interface.UserI as userService
import repository.connector.PGConnector as Connector

import logger.Logger as Logger

import hashlib


class UserService(userService.UserServiceI):
    """! 
    @brief Сервисный класс для управления операциями с пользователями
    
    Обрабатывает бизнес-логику, связанную с пользователями, включая хеширование идентификаторов,
    взаимодействие с хранилищем данных и обработку ошибок.
    
    @var connector: PostgresDBConnector - Коннектор для работы с PostgreSQL
    @var user_storage: UserRepositoryI - Репозиторий для операций с данными пользователей
    @var logger: Logger - Логгер для записи событий
    """

    def __init__(self, connector: Connector.PostgresDBConnector, user_storage: userRepository.UserRepositoryI,
                 logger: Logger.Logger):
        """!
        @brief Конструктор класса UserService
        
        @param connector: Коннектор для работы с базой данных
        @param user_storage: Репозиторий пользователей
        @param logger: Логгер для записи событий
        """
        self.connector = connector
        self.user_storage = user_storage
        self.logger = logger

    @staticmethod
    def hash_id(string: str) -> str:
        """!
        @brief Хеширует строку с использованием SHA-256
        
        @note Этот метод дублирован в коде (возможная ошибка). 
        В текущей реализации будет использоваться последняя объявленная версия.
        
        @param string: Входная строка для хеширования
        @return Хеш в виде шестнадцатеричной строки
        """
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_id(string: str) -> str:
        """!
        @brief Хеширует строку с использованием SHA-256 (дублирующий метод)
        
        @attention Метод переопределяет предыдущую реализацию с тем же именем.
        
        @param string: Входная строка для хеширования
        @return Хеш в виде шестнадцатеричной строки
        """
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, tg_id: str, chat_id: str):
        """!
        @brief Добавляет нового пользователя в хранилище
        
        @param tg_id: Идентификатор пользователя в Telegram
        @param chat_id: Идентификатор чата в Telegram
        
        @throws ValueError: При ошибках валидации данных
        @throws Exception: При других неожиданных ошибках
        
        @note Идентификаторы хешируются перед сохранением
        """
        hash_tg_id = self.hash_id(tg_id)
        hash_chat_id = self.hash_id(chat_id)
        try:
            self.user_storage.add(hash_tg_id, hash_chat_id)
            self.logger.info(f"Успешно добавлен пользователь: user_id: {tg_id}")
        except ValueError as e:
            self.logger.warning(f"Ошибка при добавлении пользователя: {e}, user_id: {tg_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении пользователя: {e}, user_id: {tg_id}")
            raise e

    def change_time_zone(self, tg_id: str, time_zone: int):
        """!
        @brief Изменяет часовой пояс пользователя
        
        @param tg_id: Идентификатор пользователя в Telegram
        @param time_zone: Новое значение часового пояса (смещение в часах)
        
        @throws ValueError: При ошибках валидации данных
        @throws Exception: При других неожиданных ошибках
        """
        hash_tg_id = self.hash_id(tg_id)
        try:
            self.user_storage.change_time_zone(hash_tg_id, time_zone)
            self.logger.info(f"Успешно изменен часовой пояс: user_id: {tg_id}")
        except ValueError as e:
            self.logger.warning(f"Ошибка при изменении часового пояса: {e}, user_id: {tg_id}")
            raise e
        except Exception as e:
            self.logger.warning(f"Ошибка при изменении часового пояса: {e}, user_id: {tg_id}")
            raise e

    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        """!
        @brief Возвращает количество событий пользователя
        
        @param tg_id: Идентификатор пользователя в Telegram
        @param chat_id: Идентификатор чата в Telegram
        
        @return Количество событий в виде целого числа
        
        @throws ValueError: При ошибках валидации данных
        @throws Exception: При других неожиданных ошибках
        """
        hash_tg_id = self.hash_id(tg_id)
        hash_chat_id = self.hash_id(chat_id)
        try:
            result = self.user_storage.get_event_count(hash_tg_id, hash_chat_id)
            self.logger.info(f"Успешно получено кол-во событий: user_id: {tg_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении кол-во событий: {e}, user_id: {tg_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении кол-во событий: {e}, user_id: {tg_id}")
            raise e

    def get_time_zone(self, tg_id: str) -> int:
        """!
        @brief Возвращает часовой пояс пользователя
        
        @param tg_id: Идентификатор пользователя в Telegram
        
        @return Часовой пояс в виде целого числа (смещение в часах)
        
        @throws ValueError: При ошибках валидации данных
        @throws Exception: При других неожиданных ошибках
        """
        hash_tg_id = self.hash_id(tg_id)

        try:
            result = self.user_storage.get_time_zone(hash_tg_id)
            self.logger.info(f"Успешно получен часовой пояс: user_id: {tg_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении часового пояса: {e}, user_id: {tg_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении часового пояса: {e}, user_id: {tg_id}")
            raise e

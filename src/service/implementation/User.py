import repository.interface.User as userRepository
import service.interface.UserI as userService
import repository.connector.PGConnector as Connector

import logger.Logger as Logger

import hashlib


class UserService(userService.UserServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, user_storage: userRepository.UserRepositoryI,
                 logger: Logger.Logger):
        self.connector = connector
        self.user_storage = user_storage
        self.logger = logger

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, tg_id: str, chat_id: str):
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



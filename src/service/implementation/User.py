import repository.interface.User as userRepository
import service.interface.UserI as userService
import repository.connector.PGConnector as Connector
import hashlib


class UserService(userService.UserServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, user_storage: userRepository.UserRepositoryI):
        self.connector = connector
        self.user_storage = user_storage

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, tg_id: str, chat_id: str):
        hash_tg_id = self.hash_id(tg_id)
        hash_chat_id = self.hash_id(chat_id)

        self.user_storage.add(hash_tg_id, hash_chat_id)

    def change_time_zone(self, tg_id: str, chat_id: str, time_zone: int):
        hash_tg_id = self.hash_id(tg_id)
        hash_chat_id = self.hash_id(chat_id)

        self.user_storage.change_time_zone(hash_tg_id, hash_chat_id, time_zone)

    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        hash_tg_id = self.hash_id(tg_id)
        hash_chat_id = self.hash_id(chat_id)

        result = self.user_storage.get_event_count(hash_tg_id, hash_chat_id)
        return result


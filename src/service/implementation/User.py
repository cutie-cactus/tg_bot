import repository.interface.User as userRepository
import service.interface.UserI as userService
import repository.connector.PGConnector as Connector


class UserService(userService.UserServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, user_storage: userRepository.UserRepositoryI):
        self.connector = connector
        self.user_storage = user_storage

    def add(self, tg_id: str, chat_id: str):
        self.user_storage.add(tg_id, chat_id)

    def change_time_zone(self, tg_id: str, chat_id: str, time_zone: int):
        self.user_storage.change_time_zone(tg_id, chat_id, time_zone)

    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        result = self.user_storage.get_event_count(tg_id, chat_id)
        return result


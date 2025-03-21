import repository.interface.User as userRepository
import repository.connector.PGConnector as Connector


class UserRepository(userRepository.UserRepositoryI):
    def __init__(self, connector: Connector.PostgresDBConnector):
        self.connector = connector

    def add(self, tg_id: str, chat_id: str):
        query = 'INSERT INTO tg_event.User (TgID , ChatID) VALUES (%s, %s) RETURNING *'
        self.connector.execute_query(query, [tg_id, chat_id], fetch=True)

    def change_time_zone(self, tg_id: str, time_zone: int):
        query = """
            UPDATE tg_event.User
            SET time_zone = %s 
            WHERE TgID = %s
        """
        self.connector.execute_query(query, [time_zone, tg_id], fetch=False)

    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        query = 'SELECT Event_count FROM tg_event.User WHERE TgID = %s AND ChatID = %s'
        event_count = self.connector.execute_query(query, [tg_id, chat_id], fetch=True)
        return event_count[0][0]

    def get_time_zone(self, tg_id: str) -> int:
        query = 'SELECT Time_zone FROM tg_event.User WHERE TgID = %s'
        event_count = self.connector.execute_query(query, [tg_id], fetch=True)
        return event_count[0][0]

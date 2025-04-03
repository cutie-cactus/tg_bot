"""!
@file UserRepository.py
@brief Репозиторий для работы с пользователями
"""

import repository.interface.User as userRepository
import repository.connector.PGConnector as Connector


class UserRepository(userRepository.UserRepositoryI):
    """!
    @brief Репозиторий для управления пользователями в системе

    @details Обеспечивает работу с основными данными пользователей:
    - Регистрация новых пользователей
    - Управление часовым поясом
    - Получение количества доступных событий
    """
    def __init__(self, connector: Connector.PostgresDBConnector):
        """!
        @brief Инициализирует репозиторий пользователей

        @param connector: Коннектор к PostgreSQL
        @type connector: Connector.PostgresDBConnector
        """
        self.connector = connector

    def add(self, tg_id: str, chat_id: str):
        """!
        @brief Добавляет нового пользователя

        @param tg_id: Идентификатор пользователя в Telegram
        @type tg_id: str
        @param chat_id: Идентификатор чата в Telegram
        @type chat_id: str

        @return Результат выполнения запроса
        """
        query = 'INSERT INTO tg_event.User (TgID , ChatID) VALUES (%s, %s) RETURNING *'
        self.connector.execute_query(query, [tg_id, chat_id], fetch=True)

    def change_time_zone(self, tg_id: str, time_zone: int):
        """!
        @brief Изменяет часовой пояс пользователя

        @param tg_id: Идентификатор пользователя в Telegram
        @type tg_id: str
        @param time_zone: Новый часовой пояс (в часах относительно UTC)
        @type time_zone: int
        """
        query = """
            UPDATE tg_event.User
            SET time_zone = %s 
            WHERE TgID = %s
        """
        self.connector.execute_query(query, [time_zone, tg_id], fetch=False)

    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        """!
        @brief Получает количество доступных событий пользователя

        @param tg_id: Идентификатор пользователя в Telegram
        @type tg_id: str
        @param chat_id: Идентификатор чата в Telegram
        @type chat_id: str

        @return Количество доступных событий
        @rtype: int
        """
        query = 'SELECT Event_count FROM tg_event.User WHERE TgID = %s AND ChatID = %s'
        event_count = self.connector.execute_query(query, [tg_id, chat_id], fetch=True)
        return event_count[0][0]

    def get_time_zone(self, tg_id: str) -> int:
        """!
        @brief Получает часовой пояс пользователя

        @param tg_id: Идентификатор пользователя в Telegram
        @type tg_id: str

        @return Часовой пояс (в часах относительно UTC)
        @rtype: int
        """
        query = 'SELECT Time_zone FROM tg_event.User WHERE TgID = %s'
        event_count = self.connector.execute_query(query, [tg_id], fetch=True)
        return event_count[0][0]

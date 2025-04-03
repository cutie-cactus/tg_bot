"""!
@file StageRepository.py
@brief Репозиторий для работы с состояниями пользователя
"""

import repository.interface.StageI as stageRepository
import repository.connector.PGConnector as Connector
from exception.Exception import *
from dto.stage import WindowType, StageType


class StageRepository(stageRepository.StageRepositoryI):
    """!
    @brief Репозиторий для управления состояниями пользователя в Telegram-боте

    @details Обеспечивает сохранение и восстановление:
    - Текущего окна (WindowType)
    - Стадии диалога (StageType)
    - Идентификаторов активных событий и напоминаний
    """
    def __init__(self, connector: Connector.PostgresDBConnector):
        """!
        @brief Инициализирует репозиторий состояний

        @param connector: Коннектор к PostgreSQL
        @type connector: Connector.PostgresDBConnector
        """
        self.connector = connector
        if not self.connector.connection:
            self.connector.connect()

    def add(self, user_id: str, window: WindowType, stage: StageType):
        """!
        @brief Добавляет или обновляет состояние пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str
        @param window: Тип активного окна
        @type window: WindowType
        @param stage: Текущая стадия диалога
        @type stage: StageType

        @return Результат выполнения запроса
        """
        query = """
            INSERT INTO tg_event.UserState (UserID, WindowTG, Stage)
            VALUES (%s, %s, %s)
            ON CONFLICT (UserID) 
            DO UPDATE SET WindowTG = EXCLUDED.WindowTG, Stage = EXCLUDED.Stage;
        """
        return self.connector.execute_query(query, [user_id, window.name, stage.name])

    def change_window(self, user_id: str, window: WindowType):
        """!
        @brief Изменяет текущее окно пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str
        @param window: Новый тип окна
        @type window: WindowType

        @return Результат выполнения запроса
        """
        query = """
            UPDATE tg_event.UserState
            SET WindowTG = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [window.name, user_id])

    def change_stage(self, user_id: str, stage: StageType):
        """!
        @brief Изменяет текущую стадию диалога

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str
        @param stage: Новая стадия диалога
        @type stage: StageType

        @return Результат выполнения запроса
        """
        query = """
            UPDATE tg_event.UserState
            SET Stage = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [stage.name, user_id])

    def change_event(self, user_id: str, event_id: int):
        """!
        @brief Устанавливает активное событие для пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str
        @param event_id: Идентификатор события
        @type event_id: int

        @return Результат выполнения запроса
        """
        query = """
            UPDATE tg_event.UserState
            SET EventID = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [event_id, user_id])

    def change_notice(self, user_id: str, notice_id: int):
        """!
        @brief Устанавливает активное напоминание для пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str
        @param notice_id: Идентификатор напоминания
        @type notice_id: int

        @return Результат выполнения запроса
        """
        query = """
            UPDATE tg_event.UserState
            SET NoticeID = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [notice_id, user_id])

    def get_stage(self, user_id: str) -> StageType:
        """!
        @brief Получает текущую стадию диалога пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str

        @return Текущая стадия или StageType.NONE если не найдено
        @rtype: StageType
        """
        query = "SELECT Stage FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            stage_name = result[0][0]
            return StageType[stage_name]
        else:
            return StageType.NONE

    def get_window(self, user_id: str) -> WindowType:
        """!
        @brief Получает текущее окно пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str

        @return Текущее окно или WindowType.MAIN_KEYBOARD если не найдено
        @rtype: WindowType
        """
        query = "SELECT WindowTG FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            window_name = result[0][0]
            return WindowType[window_name]
        else:
            return WindowType.MAIN_KEYBOARD

    def get_event(self, user_id: str) -> int:
        """!
        @brief Получает ID активного события пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str

        @return ID события или None если не установлено
        @rtype: int | None
        """
        query = "SELECT EventID FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            return result[0][0]
        return None

    def get_notice(self, user_id: str) -> int:
        """!
        @brief Получает ID активного напоминания пользователя

        @param user_id: Идентификатор пользователя Telegram
        @type user_id: str

        @return ID напоминания или None если не установлено
        @rtype: int | None
        """
        query = "SELECT NoticeID FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            return result[0][0]
        return None

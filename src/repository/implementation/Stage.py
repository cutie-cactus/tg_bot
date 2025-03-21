import repository.interface.StageI as stageRepository
import repository.connector.PGConnector as Connector
from exception.Exception import *
from dto.stage import WindowType, StageType


class StageRepository(stageRepository.StageRepositoryI):
    def __init__(self, connector: Connector.PostgresDBConnector):
        self.connector = connector
        if not self.connector.connection:
            self.connector.connect()

    def add(self, user_id: str, window: WindowType, stage: StageType):
        query = """
            INSERT INTO tg_event.UserState (UserID, WindowTG, Stage)
            VALUES (%s, %s, %s)
            ON CONFLICT (UserID) 
            DO UPDATE SET WindowTG = EXCLUDED.WindowTG, Stage = EXCLUDED.Stage;
        """
        return self.connector.execute_query(query, [user_id, window.name, stage.name])

    def change_window(self, user_id: str, window: WindowType):
        query = """
            UPDATE tg_event.UserState
            SET WindowTG = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [window.name, user_id])

    def change_stage(self, user_id: str, stage: StageType):
        query = """
            UPDATE tg_event.UserState
            SET Stage = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [stage.name, user_id])

    def change_event(self, user_id: str, event_id: int):
        query = """
            UPDATE tg_event.UserState
            SET EventID = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [event_id, user_id])

    def change_notice(self, user_id: str, notice_id: int):
        query = """
            UPDATE tg_event.UserState
            SET NoticeID = %s
            WHERE UserID = %s;
        """
        return self.connector.execute_query(query, [notice_id, user_id])

    def get_stage(self, user_id: str) -> StageType:
        query = "SELECT Stage FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            stage_name = result[0][0]
            return StageType[stage_name]
        else:
            return StageType.NONE

    def get_window(self, user_id: str) -> WindowType:
        query = "SELECT WindowTG FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            window_name = result[0][0]
            return WindowType[window_name]
        else:
            return WindowType.MAIN_KEYBOARD

    def get_event(self, user_id: str) -> int:
        query = "SELECT EventID FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            return result[0][0]
        return None

    def get_notice(self, user_id: str) -> int:
        query = "SELECT NoticeID FROM tg_event.UserState WHERE UserID = %s"
        result = self.connector.execute_query(query, [user_id], fetch=True)

        if result:
            return result[0][0]
        return None


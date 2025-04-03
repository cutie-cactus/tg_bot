"""!
@file NoticeRepository.py
@brief Реализация репозитория для работы с напоминаниями
"""

import dto.notice as noticeDTO
import model.notice as noticeModel
import repository.interface.NoticeI as noticeRepository
import repository.connector.PGConnector as Connector
from datetime import datetime, timedelta
from exception.Exception import *


class NoticeRepository(noticeRepository.NoticeRepositoryI):
    """!
    @brief Репозиторий для работы с напоминаниями в PostgreSQL

    @details Реализует CRUD-операции для напоминаний с проверкой бизнес-логики
    @var connector: Подключение к базе данных
    @type connector: Connector.PostgresDBConnector
    """
    def __init__(self, connector: Connector.PostgresDBConnector):
        """!
        @brief Инициализирует репозиторий

        @param connector: Коннектор к PostgreSQL
        @type connector: Connector.PostgresDBConnector
        """
        self.connector = connector

    def add(self, add_notice_request: noticeDTO.AddNoticeRequest) -> int:
        """!
        @brief Добавляет новое напоминание

        @param add_notice_request: DTO с данными для создания напоминания
        @type add_notice_request: noticeDTO.AddNoticeRequest

        @return ID созданного напоминания
        @rtype: int

        @throws AddNoticeException Если нет доступных слотов для напоминаний
        @throws AddNoticeTimeException Если время напоминания позже времени события
        @throws UpdateBalanceNoticeException Если не удалось обновить баланс
        """
        query_check_notice_balance = """
            SELECT Notice_count, Date, Time 
            FROM tg_event.Event 
            WHERE EventID = %s AND Notice_count > 0;
        """

        query_insert_notice = """
            INSERT INTO tg_event.Notice (EventID, Date, Time)
            VALUES (%s, %s, %s)
            RETURNING NoticeID;
        """

        query_update_notice_balance = """
            UPDATE tg_event.Event 
            SET Notice_count = Notice_count - 1 
            WHERE EventID = %s AND Notice_count > 0 
            RETURNING Notice_count;
        """

        try:
            with self.connector.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query_check_notice_balance, (add_notice_request.event_id,))
                    event_data = cursor.fetchone()
                    if not event_data:
                        raise AddNoticeException()

                    event_notice_count, event_date, event_time = event_data
                    event_datetime = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S")
                    notice_datetime = datetime.strptime(f"{add_notice_request.date} {add_notice_request.time}",
                                                        "%Y-%m-%d %H:%M:%S")

                    if notice_datetime > event_datetime:
                        raise AddNoticeTimeException()

                    cursor.execute(query_update_notice_balance, (add_notice_request.event_id,))
                    updated_notice_count = cursor.fetchone()
                    if updated_notice_count[0] <= 0:
                        raise UpdateBalanceNoticeException()

                    cursor.execute(query_insert_notice, (
                        add_notice_request.event_id,
                        add_notice_request.date,
                        add_notice_request.time
                    ))

                    notice_id = cursor.fetchone()[0]
                    conn.commit()

                    return notice_id

        except Exception as e:
            conn.rollback()
            raise e

    def get(self, notice_id: int) -> noticeModel.Notice:
        """!
        @brief Получает напоминание по ID

        @param notice_id: ID напоминания
        @type notice_id: int

        @return Найденное напоминание или None
        @rtype: noticeModel.Notice | None
        """
        query = """
                            SELECT *
                            FROM tg_event.Notice
                            WHERE NoticeID = %s
                        """
        result = self.connector.execute_query(query, [notice_id], fetch=True)
        return noticeModel.Notice(*result[0]) if result else None

    def get_all(self, event_id: int) -> list[noticeModel.Notice]:
        """!
        @brief Получает все напоминания для события

        @param event_id: ID события
        @type event_id: int

        @return Список напоминаний
        @rtype: list[noticeModel.Notice]
        """
        query = 'SELECT * FROM tg_event.Notice WHERE EventID = %s'
        result = self.connector.execute_query(query, [event_id], fetch=True)
        return [noticeModel.Notice(*row) for row in result] if result else []

    def delete(self, notice_id: int, event_id: int):
        """!
        @brief Удаляет напоминание

        @param notice_id: ID напоминания
        @type notice_id: int
        @param event_id: ID связанного события
        @type event_id: int

        @details Увеличивает счетчик доступных напоминаний на 1
        """


        query = """
                    BEGIN;

                    -- Удаляем событие из таблицы Event
                    DELETE FROM tg_event.Notice WHERE NoticeID = %s;

                    -- Увеличиваем Notice_count на 1
                    UPDATE tg_event.Event
                    SET Notice_count = Notice_count + 1
                    WHERE EventID = %s;

                    COMMIT;
                """
        return self.connector.execute_query(query, [notice_id, event_id])

    def check_exist(self, notice_id: int) -> bool:
        """!
        @brief Проверяет существование напоминания

        @param notice_id: ID напоминания
        @type notice_id: int

        @return True если напоминание существует, иначе False
        @rtype: bool
        """
        query = "SELECT 1 FROM tg_event.Notice WHERE NoticeID = %s LIMIT 1;"

        try:
            with self.connector.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (notice_id,))
                    result = cursor.fetchone()
                    return result is not None
        except Exception:
            return False

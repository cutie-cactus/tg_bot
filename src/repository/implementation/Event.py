"""!
@file EventRepository.py
@brief Реализация репозитория для работы с событиями
"""

import dto.event as eventDTO
import model.event as eventModel
import repository.interface.EventI as eventRepository
import repository.connector.PGConnector as Connector
from exception.Exception import *
from datetime import date, time, datetime


class EventRepository(eventRepository.EventRepositoryI):
    """!
    @brief Репозиторий для работы с событиями в PostgreSQL

    @details Реализует CRUD-операции для событий с проверкой бизнес-логики
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
        if not self.connector.connection:
            self.connector.connect()

    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
        """!
        @brief Добавляет новое событие

        @param add_event_request: DTO с данными для создания события
        @type add_event_request: eventDTO.AddEventRequest

        @return ID созданного события
        @rtype: int

        @throws AddEventTimeException Если время события в прошлом
        @throws AddEventException Если нет доступных слотов для событий
        @throws UpdateBalanceEventException Если не удалось обновить баланс
        """
        now = datetime.now()
        event_datetime = datetime.combine(add_event_request.date, add_event_request.time)

        if event_datetime < now:
            raise AddEventTimeException()

        query_check_balance = "SELECT Event_count FROM tg_event.User WHERE TgID = %s AND Event_count > 0;"
        query_insert_event = """
                INSERT INTO tg_event.Event (UserID, Date, Time, Name, Description)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING EventID;
            """
        query_update_balance = ("UPDATE tg_event.User SET Event_count = Event_count - 1 WHERE TgID = %s AND "
                                "Event_count > 0 RETURNING Event_count;")

        try:
            with self.connector.connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query_check_balance, (add_event_request.user_id,))
                    user_event_count = cursor.fetchone()
                    if not user_event_count:
                        raise AddEventException()

                    cursor.execute(query_update_balance, (add_event_request.user_id,))
                    updated_event_count = cursor.fetchone()
                    if updated_event_count[0] <= 0:
                        raise UpdateBalanceEventException()

                    cursor.execute(query_insert_event, (
                        add_event_request.user_id,
                        add_event_request.date,
                        add_event_request.time,
                        add_event_request.name,
                        add_event_request.description
                    ))

                    event_id = cursor.fetchone()[0]
                    conn.commit()

                    return event_id

        except Exception as e:
            conn.rollback()
            raise e

    def change(self, change_event_request: eventDTO.ChangeEventRequest):
        """!
        @brief Изменяет существующее событие

        @param change_event_request: DTO с данными для изменения
        @type change_event_request: eventDTO.ChangeEventRequest

        @return Результат выполнения операции
        @rtype: bool

        @throws NoEventException Если событие не найдено
        @throws NotCorrectFixTimeEventException Если новое время в прошлом
        """
        select_query = """
                SELECT Date, Time FROM tg_event.Event
                WHERE EventID = %s AND UserID = %s
            """
        current_event_data = self.connector.execute_query(select_query,
                                                          [change_event_request.event_id, change_event_request.user_id],
                                                          fetch=True)
        print([change_event_request.event_id, change_event_request.user_id])
        if not current_event_data:
            raise NoEventException()

        current_date, current_time = current_event_data[0]  # Получаем текущую дату и время события

        if change_event_request.date or change_event_request.time:
            change_date = change_event_request.date if change_event_request.date else current_date
            change_time = change_event_request.time if change_event_request.time else current_time
            current_datetime = f"{change_date} {change_time}"

            event_datetime_obj = datetime.strptime(current_datetime, "%Y-%m-%d %H:%M:%S")
            current_datetime_obj = datetime.now()

            if event_datetime_obj <= current_datetime_obj:
                raise NotCorrectFixTimeEventException()

        fields = []
        params = []

        if change_event_request.date:
            fields.append("Date = %s")
            params.append(change_event_request.date)
        if change_event_request.time:
            fields.append("Time = %s")
            params.append(change_event_request.time)
        if change_event_request.name:
            fields.append("Name = %s")
            params.append(change_event_request.name)
        if change_event_request.description:
            fields.append("Description = %s")
            params.append(change_event_request.description)

        if not fields:
            return False

        query = f"""
                    UPDATE tg_event.Event
                    SET {", ".join(fields)}
                    WHERE EventID = %s AND UserID = %s
                """
        params.extend([change_event_request.event_id, change_event_request.user_id])
        result = self.connector.execute_query(query, params)

        if change_event_request.date or change_event_request.time:
            # Запрос на удаление уведомлений с датой позже, чем обновленное событие
            delete_query = """
                    DELETE FROM tg_event.Notice
                    WHERE EventID = %s AND (
                        (Date > %s) OR 
                        (Date = %s AND Time > %s)
                    )
                """
            # Добавляем параметры для даты и времени события
            self.connector.execute_query(delete_query,
                                         [change_event_request.event_id, change_event_request.date,
                                          change_event_request.date,
                                          change_event_request.time])

        return result

    def delete(self, user_id: str, event_id: int):
        """!
        @brief Удаляет одно событие

        @param user_id: ID пользователя
        @type user_id: str
        @param event_id: ID события
        @type event_id: int

        @details Увеличивает счетчик доступных событий на 1
        """
        query = """
            BEGIN;

            -- Удаляем событие из таблицы Event
            DELETE FROM tg_event.Event WHERE EventID = %s AND UserID = %s;

            -- Увеличиваем Event_count на 1
            UPDATE tg_event.User
            SET Event_count = Event_count + 1
            WHERE TgID = %s;

            COMMIT;
        """
        self.connector.execute_query(query, [event_id, user_id, user_id])

    def delete_all(self, user_id: str):
        """!
        @brief Удаляет все события пользователя

        @param user_id: ID пользователя
        @type user_id: str

        @return Результат выполнения операции
        @rtype: bool

        @throws ValueError Если нет событий для удаления
        """
        count_query = 'SELECT COUNT(*) FROM tg_event.Event WHERE UserID = %s'
        event_count = self.connector.execute_query(count_query, [user_id], fetch=True)[0][0]

        if event_count > 0:
            # Начало транзакции
            query = """
                BEGIN;

                -- Удаляем все события пользователя
                DELETE FROM tg_event.Event WHERE UserID = %s;

                -- Увеличиваем Event_count на количество удаленных событий
                UPDATE tg_event.User
                SET Event_count = Event_count + %s
                WHERE TgID = %s;

                COMMIT;
            """
            return self.connector.execute_query(query, [user_id, event_count, user_id])
        else:
            raise ValueError("Нет событий для удаления.")

    def get_all(self, user_id: str) -> list[eventModel.Event]:
        """!
        @brief Получает все события пользователя

        @param user_id: ID пользователя
        @type user_id: str

        @return Список событий
        @rtype: list[eventModel.Event]
        """
        query = 'SELECT * FROM tg_event.Event WHERE UserID = %s'
        result = self.connector.execute_query(query, [user_id], fetch=True)
        return [eventModel.Event(*row) for row in result] if result else []

    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        """!
        @brief Получает конкретное событие

        @param event_id: ID события
        @type event_id: int
        @param user_id: ID пользователя
        @type user_id: str

        @return Найденное событие или None
        @rtype: eventModel.Event | None
        """
        query = """
                    SELECT *
                    FROM tg_event.Event
                    WHERE EventID = %s AND UserID = %s
                """
        result = self.connector.execute_query(query, [event_id, user_id], fetch=True)
        return eventModel.Event(*result[0]) if result else None

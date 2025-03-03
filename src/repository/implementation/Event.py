import dto.event as eventDTO
import model.event as eventModel
import repository.interface.EventI as eventRepository
import repository.connector.PGConnector as Connector


class EventRepository(eventRepository.EventRepositoryI):
    def __init__(self, connector: Connector.PostgresDBConnector):
        self.connector = connector
        if not self.connector.connection:
            self.connector.connect()

    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
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
                    # Проверка доступных событий
                    cursor.execute(query_check_balance, (add_event_request.user_id,))
                    user_event_count = cursor.fetchone()
                    if not user_event_count:
                        raise ValueError("Нет доступных событий для добавления.")

                    user_event_count = user_event_count[0]

                    # Если есть доступные события, обновляем баланс
                    cursor.execute(query_update_balance, (add_event_request.user_id,))
                    updated_event_count = cursor.fetchone()
                    if updated_event_count[0] <= 0:
                        raise ValueError("Не удалось обновить баланс событий.")

                    # Вставляем событие
                    cursor.execute(query_insert_event, (
                        add_event_request.user_id,
                        add_event_request.date,
                        add_event_request.time,
                        add_event_request.name,
                        add_event_request.description
                    ))

                    event_id = cursor.fetchone()[0]  # Получаем вставленный EventID
                    conn.commit()  # Завершаем транзакцию

                    return event_id

        except Exception as e:
            # Откатываем транзакцию в случае ошибки
            conn.rollback()
            raise e

    def change(self, change_event_request: eventDTO.ChangeEventRequest):
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

        return self.connector.execute_query(query, params)

    def delete(self, user_id: str, event_id: int):
        """Удаляет одно событие и увеличивает Event_count на 1."""
        # Начало транзакции
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
        """Удаляет все события пользователя и увеличивает Event_count на количество удаленных событий."""
        # Сначала получаем количество событий пользователя, чтобы прибавить это число к Event_count
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
        query = 'SELECT * FROM tg_event.Event WHERE UserID = %s'
        result = self.connector.execute_query(query, [user_id], fetch=True)
        return [eventModel.Event(*row) for row in result] if result else []

    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        query = """
                    SELECT *
                    FROM tg_event.Event
                    WHERE EventID = %s AND UserID = %s
                """
        result = self.connector.execute_query(query, [event_id, user_id], fetch=True)
        return eventModel.Event(*result[0]) if result else None

import psycopg2
from psycopg2.extras import DictCursor
from typing import Any, List, Optional
from exception.Exception import *
from dotenv import load_dotenv
import os


class PostgresDBConnector:
    """!
    @brief Класс для работы с PostgreSQL базой данных.

    @details Обеспечивает подключение к БД, выполнение запросов и управление соединением.
    """
    def __init__(self):
        """!
        @brief Инициализация коннектора.

        @details Загружает параметры подключения из .env файла.
        @var database: Название базы данных
        @var user: Имя пользователя БД
        @var password: Пароль пользователя
        @var host: Хост БД
        @var port: Порт подключения
        @var connection: Активное соединение с БД (None если не установлено)
        """
        load_dotenv(dotenv_path="config/config.env")

        self.database = os.getenv("database")
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.host = os.getenv("host")
        self.port = os.getenv("port")
        self.connection = None

    def connect(self):
        """!
        @brief Устанавливает соединение с базой данных.

        @throws ConnectionDBException Если не удалось подключиться к БД
        @throws Exception Другие ошибки подключения
        """
        if not self.connection:
            try:
                self.connection = psycopg2.connect(
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
            except psycopg2.Error as e:
                raise ConnectionDBException()
            except Exception as e:
                raise e

    def close(self):
        """!
        @brief Закрывает соединение с базой данных.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: Optional[List[Any]] = None, fetch: bool = False):
        """!
        @brief Выполняет SQL-запрос к базе данных.

        @param query: SQL-запрос
        @type query: str
        @param params: Параметры запроса
        @type params: Optional[List[Any]]
        @param fetch: Флаг необходимости возврата результатов
        @type fetch: bool

        @return Результаты запроса (только если fetch=True)
        @rtype: List[dict] | None

        @throws NotCorrectRequestException При ошибке выполнения запроса
        """
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
        except psycopg2.Error as e:
            self.connection.rollback()
            raise NotCorrectRequestException()

import psycopg2
from psycopg2.extras import DictCursor
from typing import Any, List, Optional
# from src.logger.Logger import Logger
from exception.Exception import *
from dotenv import load_dotenv
import os


class PostgresDBConnector:
    def __init__(self):
        load_dotenv(dotenv_path="config/config.env")

        self.database = os.getenv("database")
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.host = os.getenv("host")
        self.port = os.getenv("port")
        self.connection = None

    def connect(self):
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
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query: str, params: Optional[List[Any]] = None, fetch: bool = False):
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
        except psycopg2.Error as e:
            # self.logger.error(f"Ошибка выполнения запроса: {e}")
            self.connection.rollback()
            raise NotCorrectRequestException()

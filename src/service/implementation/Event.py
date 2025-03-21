import repository.connector.PGConnector as Connector
import service.interface.EventI as eventService
import repository.interface.EventI as eventStorage

import logger.Logger as Logger

import hashlib

import dto.event as eventDTO
import model.event as eventModel


class EventService(eventService.EventServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, event_storage: eventStorage.EventRepositoryI,
                 logger: Logger.Logger):
        self.connector = connector
        self.event_storage = event_storage
        self.logger = logger

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
        temp_user_id = add_event_request.user_id
        try:
            add_event_request.user_id = self.hash_id(temp_user_id)
            event_id = self.event_storage.add(add_event_request)
            self.logger.info(f"Успешно добавленно событие: user_id: {temp_user_id}, "
                             f"event_id: {event_id}")
            return event_id
        except ValueError as e:
            self.logger.warning(f"Ошибка при добавлении события: {e}, user_id: {temp_user_id}, "
                                f"add_event_request: {{ {', '.join(f'{k}={v}' for k, v in
                                                                   vars(add_event_request).items()
                                                                   if k != 'user_id')} }}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении события: {e}, user_id: {temp_user_id}, "
                                f"add_event_request: {{ {', '.join(f'{k}={v}' for k, v in
                                                                   vars(add_event_request).items()
                                                                   if k != 'user_id')} }}")
            raise e

    def change(self, change_event_request: eventDTO.ChangeEventRequest):
        temp_user_id = change_event_request.user_id
        try:
            change_event_request.user_id = self.hash_id(change_event_request.user_id)
            self.event_storage.change(change_event_request)
            self.logger.info(f"Успешно изменено событие: user_id: {temp_user_id}, "
                             f"event_id: {change_event_request.event_id}")
        except ValueError as e:
            self.logger.warning(f"Ошибка при изменении события: {e}, user_id: {temp_user_id}, "
                                f"change_event_request: {{ {', '.join(f'{k}={v}' for k, v in
                                                                      vars(change_event_request).items()
                                                                      if k != 'user_id')} }}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при изменении события: {e}, user_id: {temp_user_id}, "
                                f"change_event_request: {{ {', '.join(f'{k}={v}' for k, v in
                                                                      vars(change_event_request).items()
                                                                      if k != 'user_id')} }}")
            raise e

    def delete(self, user_id: str, event_id: int):
        try:
            hash_user_id = self.hash_id(user_id)
            self.event_storage.delete(hash_user_id, event_id)
            self.logger.info(f"Успешно удалено событие: user_id: {user_id}, "
                             f"event_id: {event_id}")
        except ValueError as e:
            self.logger.warning(f"Ошибка при удалении события: {e}, user_id: {user_id}, "
                                f"event_id: {event_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при удалении события: {e}, user_id: {user_id}, "
                                f"event_id: {event_id}")
            raise e

    def delete_all(self, user_id: str):
        try:
            hash_user_id = self.hash_id(user_id)
            self.event_storage.delete_all(hash_user_id)
            self.logger.info(f"Успешно удалены все события: user_id: {user_id}")
        except ValueError as e:
            self.logger.warning(f"Ошибка при удалении всех событий: {e}, user_id: {user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при удалении всех событий: {e}, user_id: {user_id}")
            raise e

    def get_all(self, user_id: str) -> list[eventModel.Event]:
        try:
            hash_user_id = self.hash_id(user_id)
            events = self.event_storage.get_all(hash_user_id)
            self.logger.info(f"Успешно полученны все события: user_id: {user_id}")
            return events
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении всех событий: {e}, user_id: {user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении всех событий: {e}, user_id: {user_id}")
            raise e

    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        try:
            hash_user_id = self.hash_id(user_id)
            event = self.event_storage.get(event_id, hash_user_id)
            self.logger.info(f"Успешно полученно событие: user_id: {user_id}, event_id: {event_id}")
            return event
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении события: {e}, user_id: {user_id}, event_id: {event_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении события: {e}, user_id: {user_id}, event_id: {event_id}")
            raise e


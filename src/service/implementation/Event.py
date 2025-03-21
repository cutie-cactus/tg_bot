import repository.connector.PGConnector as Connector
import service.interface.EventI as eventService
import repository.interface.EventI as eventStorage
import hashlib

import dto.event as eventDTO
import model.event as eventModel


class EventService(eventService.EventServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, event_storage: eventStorage.EventRepositoryI):
        self.connector = connector
        self.event_storage = event_storage

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
        add_event_request.user_id = self.hash_id(add_event_request.user_id)
        return self.event_storage.add(add_event_request)

    def change(self, change_event_request: eventDTO.ChangeEventRequest):
        change_event_request.user_id = self.hash_id(change_event_request.user_id)
        self.event_storage.change(change_event_request)

    def delete(self, user_id: str, event_id: int):
        hash_user_id = self.hash_id(user_id)
        self.event_storage.delete(hash_user_id, event_id)

    def delete_all(self, user_id: str):
        hash_user_id = self.hash_id(user_id)
        self.event_storage.delete_all(hash_user_id)

    def get_all(self, user_id: str) -> list[eventModel.Event]:
        hash_user_id = self.hash_id(user_id)
        events = self.event_storage.get_all(hash_user_id)

        return events

    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        hash_user_id = self.hash_id(user_id)
        event = self.event_storage.get(event_id, hash_user_id)
        return event

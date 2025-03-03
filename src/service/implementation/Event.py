import repository.connector.PGConnector as Connector
import service.interface.EventI as eventService
import repository.interface.EventI as eventStorage

import dto.event as eventDTO
import model.event as eventModel


class EventService(eventService.EventServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, event_storage: eventStorage.EventRepositoryI):
        self.connector = connector
        self.event_storage = event_storage

    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
        return self.event_storage.add(add_event_request)

    def change(self, change_event_request: eventDTO.ChangeEventRequest):
        self.event_storage.change(change_event_request)

    def delete(self, user_id: str, event_id: int):
        self.event_storage.delete(user_id, event_id)

    def delete_all(self, user_id: str):
        self.event_storage.delete_all(user_id)

    def get_all(self, user_id: str) -> list[eventModel.Event]:
        events = self.event_storage.get_all(user_id)
        return events

    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        event = self.event_storage.get(event_id, user_id)
        return event

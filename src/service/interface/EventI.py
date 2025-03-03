from abc import ABC, abstractmethod

import dto.event as eventDTO
import model.event as eventModel


class EventServiceI(ABC):

    @abstractmethod
    def add(self, add_event_request: eventDTO.AddEventRequest) -> int:
        pass

    @abstractmethod
    def change(self, change_event_request: eventDTO.ChangeEventRequest):
        pass

    @abstractmethod
    def delete(self, user_id: str, event_id: int):
        pass

    @abstractmethod
    def delete_all(self, user_id: str):
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> list[eventModel.Event]:
        pass

    @abstractmethod
    def get(self, event_id: int, user_id: str) -> eventModel.Event:
        pass


from abc import ABC, abstractmethod


class UserServiceI(ABC):
    @abstractmethod
    def add(self, tg_id: str, chat_id: str):
        pass

    @abstractmethod
    def change_time_zone(self, tg_id: str, chat_id: str, time_zone: int):
        pass

    @abstractmethod
    def get_event_count(self, tg_id: str, chat_id: str) -> int:
        pass



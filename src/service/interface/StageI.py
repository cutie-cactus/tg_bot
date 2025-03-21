from abc import ABC, abstractmethod

from dto.stage import WindowType, StageType


class StageServiceI(ABC):

    @abstractmethod
    def add(self, user_id: str):
        pass

    @abstractmethod
    def change_window(self, user_id: str, window: WindowType):
        pass

    @abstractmethod
    def change_stage(self, user_id: str, stage: StageType):
        pass

    @abstractmethod
    def change_event(self, user_id: str, event_id: int):
        pass

    @abstractmethod
    def change_notice(self, user_id: str, notice_id: int):
        pass

    @abstractmethod
    def get_stage(self, user_id: str) -> StageType:
        pass

    @abstractmethod
    def get_window(self, user_id: str) -> WindowType:
        pass

    @abstractmethod
    def get_event(self, user_id: str) -> int:
        pass

    @abstractmethod
    def get_notice(self, user_id: str) -> int:
        pass

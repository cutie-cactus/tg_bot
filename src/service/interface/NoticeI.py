from abc import ABC, abstractmethod

import dto.notice as noticeDTO
import model.notice as noticeModel


class NoticeServiceI(ABC):

    @abstractmethod
    def add(self, add_notice_request: noticeDTO.AddNoticeRequest) -> int:
        pass

    @abstractmethod
    def get(self, notice_id: int) -> noticeModel.Notice:
        pass

    @abstractmethod
    def get_all(self, event_id: int) -> list[noticeModel.Notice]:
        pass

    @abstractmethod
    def delete(self, notice_id: int, event_id: int):
        pass

    @abstractmethod
    def check_exist(self, notice_id: int) -> bool:
        pass

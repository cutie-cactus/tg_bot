import repository.connector.PGConnector as Connector
import service.interface.NoticeI as noticeService
import repository.interface.NoticeI as noticeStorage
import hashlib

import dto.notice as noticeDTO
import model.notice as noticeModel


class NoticeService(noticeService.NoticeServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, notice_storage: noticeStorage.NoticeRepositoryI):
        self.connector = connector
        self.notice_storage = notice_storage

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, add_notice_request: noticeDTO.AddNoticeRequest) -> int:
        add_notice_request.user_id = self.hash_id(add_notice_request.user_id)
        return self.notice_storage.add(add_notice_request)

    def get(self, notice_id: int) -> noticeModel.Notice:
        return self.notice_storage.get(notice_id)

    def get_all(self, event_id: int) -> list[noticeModel.Notice]:
        return self.notice_storage.get_all(event_id)

    def delete(self, notice_id: int, event_id: int):
        self.notice_storage.delete(notice_id, event_id)

    def check_exist(self, notice_id: int) -> bool:
        return self.notice_storage.check_exist(notice_id)


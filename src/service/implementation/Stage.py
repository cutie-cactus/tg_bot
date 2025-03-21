import repository.connector.PGConnector as Connector
import service.interface.StageI as stageService
import repository.interface.StageI as stageStorage
import logger.Logger as Logger
import hashlib

from dto.stage import WindowType, StageType


class StageService(stageService.StageServiceI):
    def __init__(self, connector: Connector.PostgresDBConnector, stage_storage: stageStorage.StageRepositoryI,
                 logger: Logger.Logger):
        self.connector = connector
        self.stage_storage = stage_storage
        self.logger = logger

    @staticmethod
    def hash_id(string: str) -> str:
        return hashlib.sha256(string.encode('utf-8')).hexdigest()

    def add(self, user_id: str):
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.add(temp_user_id, WindowType.MAIN_KEYBOARD, StageType.NONE)
            self.logger.info(f"Успешно создано состояние: user_id: {temp_user_id}")

            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при создании состояния: {e}, "
                                f"user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при создании состояния: {e}, "
                                f"user_id: {temp_user_id}")
            raise e

    def change_window(self, user_id: str, window: WindowType):
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_window(temp_user_id, window)
            self.logger.info(f"Успешно изменено состояние окна: user_id: {temp_user_id}, window: {window}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при изменении состояние окна: {e}, user_id: {temp_user_id}, window: {window}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при изменении состояние окна: {e}, user_id: {temp_user_id}, window: {window}")
            raise e

    def change_stage(self, user_id: str, stage: StageType):
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_stage(temp_user_id, stage)
            self.logger.info(f"Успешно изменено состояние ожидания: user_id: {temp_user_id}, stage: {stage}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при изменении состояние ожидания: {e}, user_id: {temp_user_id}, stage: {stage}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при изменении состояние ожидания: {e}, user_id: {temp_user_id}, stage: {stage}")
            raise e


    def change_event(self, user_id: str, event_id: int):
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_event(temp_user_id, event_id)
            self.logger.info(f"Успешно изменено выбранное событие: user_id: {temp_user_id}, event_id: {event_id}")
            return result
        except ValueError as e:
            self.logger.warning(
                f"Ошибка при изменении выбранного событие: {e}, user_id: {temp_user_id}, event_id: {event_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при изменении выбранного событие: {e}, user_id: {temp_user_id}, event_id: {event_id}")
            raise e

    def change_notice(self, user_id: str, notice_id: int):
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.change_notice(temp_user_id, notice_id)
            self.logger.info(f"Успешно изменено выбранное напоминание: user_id: {temp_user_id}, notice_id: {notice_id}")
            return result
        except ValueError as e:
            self.logger.warning(
                f"Ошибка при изменении выбранного напоминания: {e}, user_id: {temp_user_id}, notice_id: {notice_id}")
            raise e
        except Exception as e:
            self.logger.error(
                f"Ошибка при изменении выбранного напоминания: {e}, user_id: {temp_user_id}, notice_id: {notice_id}")
            raise e

    def get_stage(self, user_id: str) -> StageType:
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_stage(temp_user_id)
            self.logger.info(f"Успешно получено состояние ожидания: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении состояния ожидания: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении состояния ожидания: {e}, user_id: {temp_user_id}")
            raise e

    def get_window(self, user_id: str) -> WindowType:
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_window(temp_user_id)
            self.logger.info(f"Успешно получено состояние окна: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении состояния окна: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении состояния окна: {e}, user_id: {temp_user_id}")
            raise e

    def get_event(self, user_id: str) -> int:
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_event(temp_user_id)
            self.logger.info(f"Успешно получено выбранное событие: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении выбранного события: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении выбранного события: {e}, user_id: {temp_user_id}")
            raise e

    def get_notice(self, user_id: str) -> int:
        temp_user_id = self.hash_id(user_id)
        try:
            result = self.stage_storage.get_notice(temp_user_id)
            self.logger.info(f"Успешно получено выбранное напоминание: user_id: {temp_user_id}")
            return result
        except ValueError as e:
            self.logger.warning(f"Ошибка при получении выбранного напоминания: {e}, user_id: {temp_user_id}")
            raise e
        except Exception as e:
            self.logger.error(f"Ошибка при получении выбранного напоминания: {e}, user_id: {temp_user_id}")
            raise e

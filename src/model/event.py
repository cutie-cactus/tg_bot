from dataclasses import dataclass
from typing import Optional
from datetime import date, time


@dataclass
class Event:
    """!
    @brief Класс, представляющий событие в системе.

    @details Содержит всю информацию о событии, включая метаданные и содержание.
    Используется для хранения, передачи и обработки данных о событиях.

    @var event_id: Уникальный идентификатор события
    @type event_id: int

    @var user_id: Идентификатор пользователя, которому принадлежит событие
    @type user_id: str

    @var notice_count: Количество связанных с событием напоминаний
    @type notice_count: int

    @var date: Дата события
    @type date: datetime.date

    @var time: Время события
    @type time: datetime.time

    @var name: Название события
    @type name: str

    @var description: Подробное описание события
    @type description: str
    """
    event_id: int
    user_id: str
    notice_count: int
    date: date
    time: time
    name: str
    description: str

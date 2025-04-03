from dataclasses import dataclass
from datetime import date, time


@dataclass
class Notice:
    """!
    @brief Класс, представляющий напоминание о событии.

    @details Содержит информацию о времени напоминания и связь с соответствующим событием.

    @var notice_id: Уникальный идентификатор напоминания
    @type notice_id: int

    @var event_id: Идентификатор связанного события
    @type event_id: int

    @var date: Дата срабатывания напоминания
    @type date: datetime.date

    @var time: Время срабатывания напоминания
    @type time: datetime.time
    """
    notice_id: int
    event_id: int
    date: date
    time: time

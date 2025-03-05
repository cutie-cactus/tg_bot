from dataclasses import dataclass
from datetime import date, time


@dataclass
class Notice:
    notice_id: int
    event_id: int
    date: date
    time: time

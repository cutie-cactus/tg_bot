from dataclasses import dataclass
from typing import Optional
from datetime import date, time


@dataclass
class Event:
    event_id: int
    user_id: str
    notice_count: int
    date: date
    time: time
    name: str
    description: str



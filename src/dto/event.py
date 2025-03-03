from dataclasses import dataclass
from typing import Optional
from datetime import date, time


@dataclass
class AddEventRequest:
    user_id: str
    date: date
    time: time
    name: str
    description: str


@dataclass
class ChangeEventRequest:
    user_id: str
    event_id: int
    date: Optional[date] = None
    time: Optional[time] = None
    name: Optional[str] = None
    description: Optional[str] = None

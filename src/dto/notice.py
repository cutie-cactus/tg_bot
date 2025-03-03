from dataclasses import dataclass
from typing import Optional
from datetime import date, time


@dataclass
class AddNoticeRequest:
    event_id: int
    date: date
    time: time

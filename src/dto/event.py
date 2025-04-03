from dataclasses import dataclass
from typing import Optional
from datetime import date, time


@dataclass
class AddEventRequest:
    """!
    @brief Запрос на добавление нового события.
    
    @var user_id: Идентификатор пользователя.
    @var date: Дата события.
    @var time: Время события.
    @var name: Название события.
    @var description: Описание события.
    """
    user_id: str
    date: date
    time: time
    name: str
    description: str


@dataclass
class ChangeEventRequest:
    """!
    @brief Запрос на изменение существующего события.
    
    @details Все поля опциональны - изменяются только те, которые переданы.
    
    @var user_id: Идентификатор пользователя (обязательное поле).
    @var event_id: Идентификатор события (обязательное поле).
    @var date: Новая дата события (опционально).
    @var time: Новое время события (опционально).
    @var name: Новое название события (опционально).
    @var description: Новое описание события (опционально).
    """
    user_id: str
    event_id: int
    date: Optional[date] = None
    time: Optional[time] = None
    name: Optional[str] = None
    description: Optional[str] = None

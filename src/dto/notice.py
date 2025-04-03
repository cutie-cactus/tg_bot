@dataclass
class AddNoticeRequest:
    """!
    @brief Запрос на добавление напоминания для события.
    
    @details Содержит информацию о времени напоминания для указанного события.
    
    @var event_id: Идентификатор события, для которого устанавливается напоминание
    @var date: Дата напоминания
    @var time: Время напоминания
    """
    event_id: int
    date: date
    time: time

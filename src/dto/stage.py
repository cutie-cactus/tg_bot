from enum import Enum
from telegram import Update, ReplyKeyboardMarkup


class WindowType(Enum):
    """!
    @brief Типы клавиатурных интерфейсов бота
    
    @var MAIN_KEYBOARD: Основная клавиатура с главными командами
    @var BACK_KEYBOARD: Клавиатура с кнопкой "Назад"
    @var CHOOSE_KEYBOARD: Клавиатура выбора действий
    @var CANCEL_KEYBOARD: Клавиатура с кнопкой отмены
    @var FIX_KEYBOARD: Клавиатура для процесса редактирования
    """
    MAIN_KEYBOARD = ReplyKeyboardMarkup([["Get", "Add"], ["Info", "Choose", "Delete"]], resize_keyboard=True)
    BACK_KEYBOARD = ReplyKeyboardMarkup([["Back"]], resize_keyboard=True, one_time_keyboard=True)
    CHOOSE_KEYBOARD = ReplyKeyboardMarkup(
        [["Get", "Fix"], ["Info", "Delete event"], ["Add", "Delete notice"], ["Back"]],
        resize_keyboard=True)
    CANCEL_KEYBOARD = ReplyKeyboardMarkup([["Cancel"]], resize_keyboard=True, one_time_keyboard=True)
    FIX_KEYBOARD = ReplyKeyboardMarkup([["Cancel", "Next"]], resize_keyboard=True, one_time_keyboard=True)


class StageType(Enum):
    """!
    @brief Типы состояний (стадий) диалога с ботом
    
    @var NONE: Начальное состояние
    @var WAITING_FOR_DATE: Ожидание ввода даты
    @var WAITING_FOR_TIME: Ожидание ввода времени
    @var WAITING_FOR_NAME: Ожидание ввода названия
    @var WAITING_FOR_DESCRIPTION: Ожидание ввода описания
    @var WAITING_FOR_DELETE_ALL: Ожидание подтверждения удаления всего
    @var WAITING_FOR_DELETE_EVENT: Ожидание удаления события
    @var WAITING_FOR_DELETE_NOTICE_NUMBER: Ожидание номера напоминания для удаления
    @var WAITING_FOR_DELETE_NOTICE: Ожидание удаления напоминания
    @var WAITING_FOR_EVENT: Ожидание выбора события
    @var WAITING_FOR_DATE_NOTICE_CHOOSE: Ожидание выбора даты напоминания
    @var WAITING_FOR_TIME_NOTICE_CHOOSE: Ожидание выбора времени напоминания
    @var WAITING_FOR_FIX_DATE: Ожидание исправления даты
    @var WAITING_FOR_FIX_TIME: Ожидание исправления времени
    @var WAITING_FOR_FIX_NAME: Ожидание исправления названия
    @var WAITING_FOR_FIX_DESCRIPTION: Ожидание исправления описания
    @var WAITING_FOR_TIME_ZONE: Ожидание ввода часового пояса
    @var WAITING_FOR_DELETE_NOTICE_CHOOSE: Ожидание выбора напоминания для удаления
    @var BACK: Состояние возврата назад
    """
    NONE = "none"
    WAITING_FOR_DATE = "waiting_for_date"
    WAITING_FOR_TIME = "waiting_for_time"
    WAITING_FOR_NAME = "waiting_for_name"
    WAITING_FOR_DESCRIPTION = "waiting_for_description"
    WAITING_FOR_DELETE_ALL = "waiting_for_delete_all"
    WAITING_FOR_DELETE_EVENT = "waiting_for_delete_event"
    WAITING_FOR_DELETE_NOTICE_NUMBER = "waiting_for_delete_notice_number"
    WAITING_FOR_DELETE_NOTICE = "waiting_for_delete_notice"
    WAITING_FOR_EVENT = "waiting_for_event"
    WAITING_FOR_DATE_NOTICE_CHOOSE = "waiting_for_date_notice_choose"
    WAITING_FOR_TIME_NOTICE_CHOOSE = "waiting_for_time_notice_choose"
    WAITING_FOR_FIX_DATE = "waiting_for_fix_date"
    WAITING_FOR_FIX_TIME = "waiting_for_fix_time"
    WAITING_FOR_FIX_NAME = "waiting_for_fix_name"
    WAITING_FOR_FIX_DESCRIPTION = "waiting_for_fix_description"
    WAITING_FOR_TIME_ZONE = "waiting_for_time_zone"
    WAITING_FOR_DELETE_NOTICE_CHOOSE = "waiting_for_date_notice_choose"
    BACK = "back"

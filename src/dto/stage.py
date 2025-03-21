from enum import Enum
from telegram import Update, ReplyKeyboardMarkup


class WindowType(Enum):
    MAIN_KEYBOARD = ReplyKeyboardMarkup([["Get", "Add"], ["Info", "Choose", "Delete"]], resize_keyboard=True)
    BACK_KEYBOARD = ReplyKeyboardMarkup([["Back"]], resize_keyboard=True, one_time_keyboard=True)
    CHOOSE_KEYBOARD = ReplyKeyboardMarkup(
        [["Get", "Fix"], ["Info", "Delete event"], ["Add", "Delete notice"], ["Back"]],
        resize_keyboard=True)
    CANCEL_KEYBOARD = ReplyKeyboardMarkup([["Cancel"]], resize_keyboard=True, one_time_keyboard=True)
    FIX_KEYBOARD = ReplyKeyboardMarkup([["Cancel", "Next"]], resize_keyboard=True, one_time_keyboard=True)


class StageType(Enum):
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

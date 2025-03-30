import pytest
# from handlers import is_valid_date, is_valid_time, is_valid_time_zone
from datetime import datetime, timedelta
import re


def is_valid_date(date_str: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return False

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_obj >= datetime.today().date()
    except ValueError:
        return False


def is_valid_time_zone(time_zone: str) -> bool:
    print(bool(re.match(r"^[+-]([0-9]|[0-9]{2})$", time_zone)))
    if not bool(re.match(r"^[+-]([0-9]|[0-9]{2})$", time_zone)):
        return False

    return -12 <= int(time_zone) <= 14


def is_valid_time(date_str: str, time_str: str) -> bool:
    if not re.fullmatch(r"\d{2}:\d{2}", time_str):
        return False

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%H:%M").time()

        now = datetime.now()
        now_date, now_time = now.date(), now.time()

        return date_obj > now_date or (date_obj == now_date and time_obj > now_time)

    except ValueError:
        return False


def test_is_valid_date():
    today = datetime.today().strftime("%Y-%m-%d")
    future_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    past_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    assert is_valid_date(today) is True, "Сегодняшняя дата должна быть валидной"
    assert is_valid_date(future_date) is True, "Будущая дата должна быть валидной"
    assert is_valid_date(past_date) is False, "Прошедшая дата должна быть невалидной"
    assert is_valid_date("2024-13-01") is False, "Некорректная дата должна быть невалидной"
    assert is_valid_date("abcd-ef-gh") is False, "Строка не в формате YYYY-MM-DD должна быть невалидной"


def test_is_valid_time_zone():
    assert is_valid_time_zone("+3") is True, "Часовой пояс +3 должен быть валиден"
    assert is_valid_time_zone("-5") is True, "Часовой пояс -5 должен быть валиден"
    assert is_valid_time_zone("-12") is True, "Часовой пояс -12 должен быть валиден"
    assert is_valid_time_zone("-13") is False, "Часовой пояс -13 не должен быть валиден"
    assert is_valid_time_zone("15") is False, "Часовой пояс 15 не должен быть валиден"
    assert is_valid_time_zone("abc") is False, "Некорректный ввод должен быть невалидным"
    assert is_valid_time_zone("+10:30") is False, "Часовой пояс с минутами не должен быть валиден"


def test_is_valid_time():
    today = datetime.today().strftime("%Y-%m-%d")
    now_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
    past_time = (datetime.now() - timedelta(minutes=1)).strftime("%H:%M")
    future_date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    assert is_valid_time(today, now_time) is True, "Текущее время +1 минута должно быть валидным"
    assert is_valid_time(today, past_time) is False, "Текущее время -1 минута не должно быть валидным"
    assert is_valid_time(future_date, "00:00") is True, "Любое время на будущую дату должно быть валидным"
    assert is_valid_time("2024-13-01", "12:00") is False, "Некорректная дата должна быть невалидной"
    assert is_valid_time(today, "25:00") is False, "Некорректное время не должно быть валидным"
    assert is_valid_time(today, "abcd") is False, "Строка не в формате HH:MM должна быть невалидной"

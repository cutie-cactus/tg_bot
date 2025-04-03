import repository.connector.PGConnector as Connector
import service.implementation.Event as eventService
import repository.implementation.Event as eventStorage
import service.implementation.Notice as noticeService
import repository.implementation.Notice as noticeStorage
import service.implementation.User as userService
import repository.implementation.User as userStorage
import service.implementation.Stage as stageService
import repository.implementation.Stage as stageStorage
import dto.event as eventDTO
import model.event as eventModel
import dto.notice as noticeDTO
import model.notice as noticeModel
import logger.Logger as Logger
from dto.stage import WindowType, StageType
from exception.Exception import *
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, JobQueue
from datetime import datetime, timedelta
import re

"""@var
@brief Инициализация базовых компонентов системы
@var connector - Подключение к PostgreSQL
@var logger - Логгер системы
"""
connector = Connector.PostgresDBConnector()
logger = Logger.Logger()

"""@var
@brief Репозитории и сервисы событий
@var event_repository - Хранилище операций с событиями
@var event_service - Бизнес-логика работы с событиями
"""
event_repository = eventStorage.EventRepository(connector)
event_service = eventService.EventService(connector, event_repository, logger)

"""@var
@brief Репозитории и сервисы уведомлений
@var notice_repository - Хранилище операций с уведомлениями
@var notice_service - Бизнес-логика работы с уведомлениями
"""
notice_repository = noticeStorage.NoticeRepository(connector)
notice_service = noticeService.NoticeService(connector, notice_repository, logger)

"""@var
@brief Репозитории и сервисы пользователей
@var user_repository - Хранилище операций с пользователями
@var user_service - Бизнес-логика работы с пользователями
"""
user_repository = userStorage.UserRepository(connector)
user_service = userService.UserService(connector, user_repository, logger)

"""@var
@brief Репозитории и сервисы состояний
@var stage_repository - Хранилище операций с состояниями
@var stage_service - Бизнес-логика работы с состояниями
"""
stage_repository = stageStorage.StageRepository(connector)
stage_service = stageService.StageService(connector, stage_repository, logger)

"""@var
@brief Клавиатуры интерфейса
@var MAIN_KEYBOARD - Основное меню
@var BACK_KEYBOARD - Кнопка возврата
@var CHOOSE_KEYBOARD - Меню выбора события
@var CANCEL_KEYBOARD - Кнопка отмены
@var FIX_KEYBOARD - Кнопки для редактирования
"""
MAIN_KEYBOARD = ReplyKeyboardMarkup([["Get", "Add"], ["Info", "Choose", "Delete"]], resize_keyboard=True)
BACK_KEYBOARD = ReplyKeyboardMarkup([["Back"]], resize_keyboard=True, one_time_keyboard=True)
CHOOSE_KEYBOARD = ReplyKeyboardMarkup([["Get", "Fix"], ["Info", "Delete event"], ["Add", "Delete notice"], ["Back"]],
                                      resize_keyboard=True)
CANCEL_KEYBOARD = ReplyKeyboardMarkup([["Cancel"]], resize_keyboard=True, one_time_keyboard=True)
FIX_KEYBOARD = ReplyKeyboardMarkup([["Cancel", "Next"]], resize_keyboard=True, one_time_keyboard=True)

"""@var
@brief Текстовые шаблоны
@var INFO_CHOOSE_TEXT - Информация в режиме выбора события
@var INFO_MAIN_TEXT - Информация в главном меню
"""
INFO_CHOOSE_TEXT = (
    "🔔 *Добро пожаловать!* 🔔\n\n"
    "Этот бот помогает вам управлять вашими событиями и уведомлениями.\n"
    "Сейчас вы находитель в меню события.\n\n"
    "*Доступные команды:*\n"
    "*Get* – получить информацию о событии и его напоминаниях\n"
    "*Fix* – изменить выбранное событие\n"
    "*Info* – информация о боте\n"
    "*Delete event* – удалить выбранное событие\n"
    "*Add* – добавить новое напоминание у события\n"
    "*Delete notice* – удалить напоминание у события\n"
    "*Back* – вернуться в главное меню\n\n"
    "Если у вас есть вопросы, напишите в поддержку: *@Sksjdjcj*"
)

INFO_MAIN_TEXT = (
    "🔔 *Добро пожаловать!* 🔔\n\n"
    "Этот бот помогает вам управлять вашими событиями и уведомлениями.\n"
    "Сейчас вы находитель в главном меню.\n\n"
    "*Доступные команды:*\n"
    "*Get* – получить список ваших событий\n"
    "*Add* – добавить новое событие\n"
    "*Info* – информация о боте\n"
    "*Choose* – выбрать конкретное событие, для дальнейшей работы с ним\n"
    "*Delete* – удалить все ваши события\n\n"
    "Если у вас есть вопросы, напишите в поддержку: *@Sksjdjcj*"
)


def is_valid_date(date_str: str) -> bool:
    """@var
    @brief Валидатор формата даты
    @param date_str[in] - Строка даты в формате ГГГГ-ММ-ДД
    @return bool - Валидность даты
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return False

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_obj >= datetime.today().date()
    except ValueError:
        return False


def is_valid_time_zone(time_zone: str) -> bool:
    """@var
    @brief Валидатор часового пояса
    @param time_zone[in] - Строка смещения UTC
    @return bool - Валидность значения
    """
    if not bool(re.match(r"^[+-]([0-9]|[0-9]{2})$", time_zone)):
        return False

    return -12 <= int(time_zone) <= 14


def is_valid_time(date_str: str, time_str: str) -> bool:
    """@var
    @brief Валидатор времени события
    @param date_str[in] - Дата события
    @param time_str[in] - Время события
    @return bool - Валидность времени
    """
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


async def start(update: Update, context: CallbackContext) -> None:
    """@var
    @brief Обработчик команды /start
    @param update[in] - Объект обновления Telegram
    @param context[in] - Контекст выполнения
    """
    keyboard = [["Старт"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Нажмите 'Старт' для продолжения:", reply_markup=reply_markup)


async def show_main_menu(update: Update, context: CallbackContext) -> None:
    """@var
    @brief Инициализация нового пользователя
    @details Регистрирует пользователя и запрашивает часовой пояс
    @var chat_id - Идентификатор чата
    @var tg_id - Идентификатор пользователя Telegram
    """
    stage_service.change_window(str(update.message.from_user.id), WindowType.MAIN_KEYBOARD)

    chat_id = update.message.chat.id
    tg_id = update.message.from_user.id
    try:
        user_service.add(str(tg_id), str(chat_id))
    except Exception as e:
        print(e)

    try:
        stage_service.add(str(tg_id))
    except Exception as e:
        print(e)

    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_TIME_ZONE)
    await update.message.reply_text("Введите ваш часовой пояс (+/- <число>):")


async def back_to_main_menu(update: Update, context: CallbackContext) -> None:
    """@var
    @brief Возврат в главное меню
    @details Сбрасывает привязанные события/уведомления
    """
    stage_service.change_window(str(update.message.from_user.id), WindowType.MAIN_KEYBOARD)
    stage_service.change_notice(str(update.message.from_user.id), None)
    stage_service.change_event(str(update.message.from_user.id), None)

    await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=MAIN_KEYBOARD)


async def next_to_fix_event(update: Update, context: CallbackContext) -> None:
    """@var
    @brief Навигация по этапам редактирования
    @details Управляет контекстом редактирования через user_data
    @var stage - Текущий этап редактирования
    @var fix_date - Новая дата события
    @var fix_time - Новое время события
    """
    stage = stage_service.get_stage(str(update.message.from_user.id)).value
    if stage == 'waiting_for_fix_date':
        context.user_data["fix_date"] = None
        stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_FIX_TIME)

        await update.message.reply_text(
            "Вы пропустили изменение даты.\n\nВведите новое время события (ЧЧ:ММ) или нажмите 'Назад':",
            reply_markup=FIX_KEYBOARD)
    elif stage == 'waiting_for_fix_time':
        context.user_data["fix_time"] = None
        stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_FIX_NAME)

        await update.message.reply_text(
            "Вы пропустили изменение времени.\n\nВведите новое название события или нажмите 'Назад':",
            reply_markup=FIX_KEYBOARD)
    elif stage == 'waiting_for_fix_name':
        context.user_data["fix_name"] = None
        stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_FIX_DESCRIPTION)

        await update.message.reply_text(
            "Вы пропустили изменение названия.\n\nВведите новое описание события или нажмите 'Назад':",
            reply_markup=FIX_KEYBOARD)
    elif stage == 'waiting_for_fix_description':
        try:
            stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)
            fix_date = datetime.strptime(context.user_data['fix_date'], "%Y-%m-%d").date() \
                if context.user_data['fix_date'] is not None else None
            fix_time = datetime.strptime(context.user_data['fix_time'], "%H:%M").time() \
                if context.user_data['fix_time'] is not None else None

            selected_event = stage_service.get_event(str(update.message.from_user.id))

            event_service.change(eventDTO.ChangeEventRequest(str(update.message.from_user.id),
                                                             selected_event,
                                                             fix_date, fix_time,
                                                             context.user_data['fix_name'],
                                                             None
                                                             ))
            await update.message.reply_text("Вы пропустили изменение описания\n\nСобытие было изменено",
                                            reply_markup=CHOOSE_KEYBOARD)
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}", reply_markup=CHOOSE_KEYBOARD)

    else:
        await update.message.reply_text("Вы вернулись в меню события.", reply_markup=CHOOSE_KEYBOARD)


async def handle_actions(update: Update, context: CallbackContext) -> None:
    """Обрабатывает нажатие кнопок, учитывая, в каком меню находится пользователь."""
    """@function
    @brief Центральный роутер действий пользователя
    @details Обрабатывает нажатия кнопок в зависимости от текущего активного меню
    
    @param update[in] - Объект обновления Telegram
    @param context[in] - Контекст выполнения
    @var text - Текст сообщения пользователя
    @var menu - Текущее активное меню (MAIN_KEYBOARD/CHOOSE_KEYBOARD)
    """
    text = update.message.text
    menu = stage_service.get_window(str(update.message.from_user.id)).name
    print(menu)
    if menu == "MAIN_KEYBOARD":
        """@branch
        @brief Обработка главного меню
        @var Get - Запрос списка событий
        @var Add - Инициализация создания события
        @var Info - Показать справку
        @var Delete - Удаление всех событий
        @var Choose - Выбор конкретного события
        """
        if text == "Get":
            await get_all_event(update, context)
            return
        elif text == "Add":
            await add_data(update, context)
            return
        elif text == "Info":
            await get_info_main(update, context)
            return
        elif text == "Delete":
            await delete_all_data(update, context)
            return
        elif text == "Choose":
            await choose_event(update, context)
            return
        stage_service.change_window(str(update.message.from_user.id), WindowType.MAIN_KEYBOARD)
        await update.message.reply_text("Обработка завершена. Возвращаюсь в главное меню.", reply_markup=MAIN_KEYBOARD)

    elif menu == "CHOOSE_KEYBOARD":
        """@branch
        @brief Обработка меню работы с событием
        @var Get - Показать уведомления события
        @var Fix - Редактирование события
        @var Delete event - Удаление текущего события
        @var Delete notice - Удаление уведомления
        @var Add - Добавление уведомления
        """
        if text == "Get":
            await get_all_notice(update, context)
            return
        elif text == "Fix":
            await fix_event(update, context)
            return
        elif text == "Info":
            await get_info_choose(update, context)
            return
        elif text == "Delete event":
            await delete_event(update, context)
            return
        elif text == "Delete notice":
            await delete_notice(update, context)
            return
        elif text == "Add":
            await add_notice(update, context)
            return

        stage_service.change_window(str(update.message.from_user.id), WindowType.CHOOSE_KEYBOARD)
        await update.message.reply_text("Обработка завершена. Возвращаюсь в меню Choose.", reply_markup=CHOOSE_KEYBOARD)


async def handle_cancel(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Обработчик отмены действий
    @details Возвращает в предыдущее меню и сбрасывает состояние
    
    @var stage - Текущий этап взаимодействия
    @var previous_menu - Предыдущее активное меню
    """
    stage = stage_service.get_stage(str(update.message.from_user.id))
    previous_menu = stage_service.get_window(str(update.message.from_user.id))
    if stage == "back":
        stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)
        await update.message.reply_text("Вы вернулись в предыдущее меню.", reply_markup=previous_menu.value)
        return

    stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)
    await update.message.reply_text("Вы вернулись в предыдущее меню.", reply_markup=previous_menu.value)


async def add_data(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Инициализация процесса добавления события
    @details Устанавливает состояние WAITING_FOR_DATE и запрашивает дату
    
    @throws Меняет состояние через stage_service
    """
    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DATE)
    await update.message.reply_text("Введите дату события (в формате ГГГГ-ММ-ДД) или нажмите 'Отмена':",
                                    reply_markup=CANCEL_KEYBOARD)


def prepare_list_event(user_id: int):
    """@var
    @brief Форматирует список событий для вывода
    @param user_id[in] - Идентификатор пользователя
    @return str - Отформатированный текст со списком
    """
    events = event_service.get_all(str(user_id))

    if not events:
        return []

    events_text = "Список ваших событий:\n\n"

    for i, event in enumerate(events, start=1):
        events_text += (f"```Событие_#{i}\n"
                        f"Дата: {event.date}\n"
                        f"Время: {str(event.time)[:5]}\n"
                        f"Уведомлений: {10 - event.notice_count}\n"
                        f"Название: {event.name}\n"
                        f"Описание: {event.description}\n"
                        f"```\n")
    return events_text


def prepare_one_event(event_id: int, user_id: int):
    """@var
    @brief Форматирует детали одного события
    @param event_id[in] - Идентификатор события
    @return str - Отформатированный текст с деталями
    """
    selected_event = event_service.get(event_id,
                                       str(user_id))

    notice_text = (f"```Событие\n"
                   f"Дата: {selected_event.date}\n"
                   f"Время: {str(selected_event.time)[:5]}\n"
                   f"Уведомлений: {10 - selected_event.notice_count}\n"
                   f"Название: {selected_event.name}\n"
                   f"Описание: {selected_event.description}\n"
                   f"```\n")

    return notice_text


def prepare_list_notice(event_id: int, user_id: int):
    """@function
    @brief Формирует текстовое представление события и его уведомлений
    @param event_id[in] - ID целевого события
    @param user_id[in] - ID пользователя для проверки прав доступа
    @return tuple (текст для отображения, флаг наличия уведомлений)
    
    @var selected_event - Объект события из event_service
    @var notices - Список уведомлений события
    @var notice_text - Буфер для формирования ответа
    @var flag - Индикатор наличия уведомлений (True/False)
    """
    selected_event = event_service.get(event_id,
                                       str(user_id))

    notices = notice_service.get_all(selected_event.event_id)

    notice_text = (f"```Событие\n"
                   f"Дата: {selected_event.date}\n"
                   f"Время: {str(selected_event.time)[:5]}\n"
                   f"Уведомлений: {10 - selected_event.notice_count}\n"
                   f"Название: {selected_event.name}\n"
                   f"Описание: {selected_event.description}\n"
                   f"```\n")

    flag = True
    if notices:
        notice_text += "Список уведомлений:\n\n"

        for i, notice in enumerate(notices, start=1):
            notice_text += (f"```Уведомление_#{i}\n"
                            f"Дата: {notice.date}\n"
                            f"Время: {str(notice.time)[:5]}\n"
                            f"```\n")
    else:
        flag = False
        notice_text += "У вас нет уведомлений для данного события."

    return notice_text, flag


async def get_all_event(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Обработчик команды получения списка событий
    @var events_text - Форматированный список событий
    @var context.user_data["menu"] - Текущее меню пользователя
    """
    context.user_data["menu"] = context.user_data.get("menu", "main")
    events_text = prepare_list_event(update.message.from_user.id)

    if not events_text:
        await update.message.reply_text("У вас нет событий.", reply_markup=MAIN_KEYBOARD)
        return

    await update.message.reply_text(events_text, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')


async def get_info_main(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Отображение информации главного меню
    @details Выводит форматированное сообщение с инструкциями для основного интерфейса
    @var INFO_MAIN_TEXT - Текстовый шаблон с markdown-разметкой
    """
    await update.message.reply_text(INFO_MAIN_TEXT, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')


async def get_info_choose(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Отображение информации меню работы с событием
    @details Выводит специализированную справку для режима редактирования
    @var INFO_CHOOSE_TEXT - Текст с описанием доступных команд
    """
    await update.message.reply_text(INFO_CHOOSE_TEXT, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')

async def choose_event(update: Update, context: CallbackContext) -> None:
    """@function 
    @brief Обработчик выбора конкретного события
    @var events_text - Форматированный список событий
    @var context.user_data["state"] - Новое состояние диалога
    @throws Переводит в состояние WAITING_FOR_EVENT через stage_service
    """
    context.user_data["menu"] = context.user_data.get("menu", "main")
    events_text = prepare_list_event(update.message.from_user.id)

    if not events_text:
        await update.message.reply_text("У вас нет событий.", reply_markup=MAIN_KEYBOARD)
        return

    await update.message.reply_text(events_text, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')

    context.user_data["state"] = "waiting_for_event"
    await update.message.reply_text("Введите номер событие или нажмите 'Отмена':",
                                    reply_markup=CANCEL_KEYBOARD)

    return notice_text



def prepare_list_notice(event_id: int, user_id: int):
    """@function
    @brief Формирует детализированный отчет о событии и уведомлениях
    @param event_id[in] - ID анализируемого события
    @param user_id[in] - Идентификатор пользователя для проверки прав
    @return tuple (текстовый отчет, флаг наличия уведомлений)
    
    @var selected_event - Объект события из event_service
    @var notices - Список связанных уведомлений
    @var notice_text - Буфер для накопления вывода
    @var flag - Индикатор наличия данных (True - есть уведомления)
    """
    selected_event = event_service.get(event_id,
                                       str(user_id))
    notice_text, _ = prepare_list_notice(context.user_data.get("selected_event").event_id,
                                         update.message.from_user.id)


    await update.message.reply_text(notice_text, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')

    notice_text = (f"```Событие\n"
                   f"Дата: {selected_event.date}\n"
                   f"Время: {str(selected_event.time)[:5]}\n"
                   f"Уведомлений: {10 - selected_event.notice_count}\n"
                   f"Название: {selected_event.name}\n"
                   f"Описание: {selected_event.description}\n"
                   f"```\n")

    flag = True
    if notices:
        notice_text += "Список уведомлений:\n\n"

        for i, notice in enumerate(notices, start=1):
            notice_text += (f"```Уведомление_#{i}\n"
                            f"Дата: {notice.date}\n"
                            f"Время: {str(notice.time)[:5]}\n"
                            f"```\n")
    else:
        flag = False
        notice_text += "У вас нет уведомлений для данного события."

    return notice_text, flag


async def get_all_event(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Получение и отображение списка всех событий
    @var events_text - Отформатированный список событий
    @throws При отсутствии событий выводит соответствующее уведомление
    """
    events_text = prepare_list_event(update.message.from_user.id)

    if not events_text:
        await update.message.reply_text("У вас нет событий.", reply_markup=MAIN_KEYBOARD)
        return

    await update.message.reply_text(events_text, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')


async def get_info_main(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Обработчик выбора события для детальной работы
    @details Инициирует состояние WAITING_FOR_EVENT для последующего ввода номера
    @var events_text - Список доступных событий
    @throws При отсутствии событий прерывает операцию
    """
    await update.message.reply_text(INFO_MAIN_TEXT, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')


async def get_info_choose(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Отображение уведомлений выбранного события
    @var selected_event - Текущее событие из stage_service
    @var notice_text - Форматированная информация о напоминаниях
    """
    await update.message.reply_text(INFO_CHOOSE_TEXT, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')


async def choose_event(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Инициализация удаления всех событий
    @details Запрашивает подтверждение перед выполнением
    @var events_text - Список событий для визуализации
    @throws Переводит в состояние WAITING_FOR_DELETE_ALL
    """
    events_text = prepare_list_event(update.message.from_user.id)

    if not events_text:
        await update.message.reply_text("У вас нет событий.", reply_markup=MAIN_KEYBOARD)
        return

    await update.message.reply_text(events_text, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')

    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_EVENT)
    print(stage_service.get_stage(str(update.message.from_user.id)))
    await update.message.reply_text("Введите номер событие или нажмите 'Отмена':",
                                    reply_markup=CANCEL_KEYBOARD)


async def get_all_notice(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Отображение всех уведомлений выбранного события
    @details Получает привязанное событие и формирует список его уведомлений
    
    @var selected_event - Текущее выбранное событие из stage_service
    @var notice_text - Форматированная строка с информацией о событии и уведомлениях
    @var events_text - Неиспользуемая переменная (возможная ошибка в коде)
    """
    selected_event = stage_service.get_event(str(update.message.from_user.id))
    notice_text, _ = prepare_list_notice(selected_event,
                                         update.message.from_user.id)

    await update.message.reply_text(notice_text, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')


    await update.message.reply_text(events_text, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')

async def delete_all_data(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Инициирует процесс удаления всех событий
    @details Показывает список событий и запрашивает подтверждение удаления
    
    @var events_text - Отформатированный список всех событий пользователя
    @throws EventNotFoundException если события отсутствуют
    """
    events_text = prepare_list_event(update.message.from_user.id)

    if not events_text:
        await update.message.reply_text("У вас нет событий.", reply_markup=MAIN_KEYBOARD)
        return

    await update.message.reply_text(events_text, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')

    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DELETE_ALL)

    await update.message.reply_text("Вы уверены что хотите удалить все события? Да/Нет",
                                    reply_markup=CANCEL_KEYBOARD)


async def delete_event(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Удаление конкретного события
    @var selected_event - Выбранное событие из stage_service
    @var event_text - Форматированная информация о событии
    @throws Переводит в состояние WAITING_FOR_DELETE_EVENT
    """
    selected_event = stage_service.get_event(str(update.message.from_user.id))

    event_text = prepare_one_event(selected_event,
                                   update.message.from_user.id)

    if not event_text:
        stage_service.change_window(str(update.message.from_user.id), WindowType.MAIN_KEYBOARD)

        await update.message.reply_text("У вас данного события.", reply_markup=MAIN_KEYBOARD)
        return

    await update.message.reply_text(event_text, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')

    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DELETE_EVENT)

    await update.message.reply_text("Вы уверены что хотите удалить данное события? Да/Нет",
                                    reply_markup=CANCEL_KEYBOARD)


async def delete_notice(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Удаление уведомления события
    @details Получает список уведомлений и инициирует процесс удаления
    
    @var selected_event - Текущее событие из stage_service
    @var notice_text - Форматированная информация об уведомлениях
    @var flag - Флаг наличия уведомлений (True - есть данные)
    """
    selected_event = stage_service.get_event(str(update.message.from_user.id))

    notice_text, flag = prepare_list_notice(selected_event,

                                            update.message.from_user.id)

    await update.message.reply_text(notice_text, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')

    if not flag:
        return

    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DELETE_NOTICE_NUMBER)

    await update.message.reply_text("Введите номер напоминания для удаления",
                                    reply_markup=CANCEL_KEYBOARD)


async def add_notice(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Инициализация добавления уведомления
    @details Устанавливает состояние ожидания выбора даты напоминания
    
    @var StageType.WAITING_FOR_DELETE_NOTICE_CHOOSE - Состояние выбора даты
    """
    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DELETE_NOTICE_CHOOSE)
    await update.message.reply_text("Введите дату напоминания (в формате ГГГГ-ММ-ДД) или нажмите 'Отмена':",
                                    reply_markup=CANCEL_KEYBOARD)


async def fix_event(update: Update, context: CallbackContext) -> None:
    """@function
    @brief Редактирование события
    @details Показывает текущие данные события и запускает процесс редактирования
    
    @var WindowType.CHOOSE_KEYBOARD - Меню действий с событием
    @var selected_event - Выбранное событие из stage_service
    @var event_text - Форматированное описание события
    @var StageType.WAITING_FOR_FIX_DATE - Состояние ожидания новой даты
    """
    stage_service.change_window(str(update.message.from_user.id), WindowType.CHOOSE_KEYBOARD)
    selected_event = stage_service.get_event(str(update.message.from_user.id))

    event_text = prepare_one_event(selected_event,
                                   update.message.from_user.id)

    if not event_text:
        stage_service.change_window(str(update.message.from_user.id), WindowType.MAIN_KEYBOARD)

        await update.message.reply_text("У вас данного события.", reply_markup=MAIN_KEYBOARD)
        return

    await update.message.reply_text(event_text, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')

    stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_FIX_DATE)
    await update.message.reply_text("Введите новую дату события (в формате ГГГГ-ММ-ДД) или нажмите 'Отмена':",

                                    reply_markup=FIX_KEYBOARD)


async def handle_user_input(update: Update, context: CallbackContext) -> None:
    """@var
    @brief Центральный обработчик ввода пользователя
    @details Анализирует состояние через stage_service
    @var text - Текст сообщения пользователя
    @var state - Текущее состояние из stage_service
    @var context.user_data - Хранилище временных данных
    @var selected_event - Выбранное событие
    @var delay - Задержка для уведомления
    """

    text = update.message.text
    state = stage_service.get_stage(str(update.message.from_user.id)).value
    print(state)
    if state == "waiting_for_date":
        if is_valid_date(text):
            context.user_data["date"] = text
            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_TIME)

            await update.message.reply_text("Введите время события (в формате ЧЧ:ММ) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)
        else:
            await update.message.reply_text("Введите дату события (в формате ГГГГ-ММ-ДД) или нажмите 'Отмена':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_time":
        if is_valid_time(context.user_data['date'], text):
            context.user_data["time"] = text
            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_NAME)

            await update.message.reply_text("Введите название события или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)
        else:
            await update.message.reply_text("Введите время события (в формате ЧЧ:ММ) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_name":
        context.user_data["name"] = text
        stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DESCRIPTION)

        await update.message.reply_text("Введите описание события или нажмите 'Назад':", reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_description":
        context.user_data["description"] = text
        try:
            event_id = event_service.add(eventDTO.AddEventRequest(str(update.message.from_user.id),
                                                                                       datetime.strptime(
                                                                                           context.user_data['date'],
                                                                                           "%Y-%m-%d").date(),
                                                                                       datetime.strptime(
                                                                                           context.user_data['time'],
                                                                                           "%H:%M").time(),
                                                                                       context.user_data['name'],
                                                                                       context.user_data['description']))
            stage_service.change_event(str(update.message.from_user.id), event_id)
            await update.message.reply_text("Событие было успешно создано",
                                            reply_markup=MAIN_KEYBOARD)
        except AddEventTimeException as e:
            await update.message.reply_text(f'{e}', reply_markup=MAIN_KEYBOARD)
        except Exception as e:
            await update.message.reply_text(f'Не удалось создать событие', reply_markup=MAIN_KEYBOARD)

        stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)


    elif state == "waiting_for_delete_all":
        stage_service.change_stage(str(update.message.from_user.id), StageType.BACK)


        if text.lower() == 'да':
            try:
                event_service.delete_all(str(update.message.from_user.id))
                await update.message.reply_text("Успешно удалилось.", reply_markup=MAIN_KEYBOARD)
            except Exception as e:
                await update.message.reply_text(f"{e}", reply_markup=MAIN_KEYBOARD)
        else:
            await update.message.reply_text("Вы решили не удалять.", reply_markup=MAIN_KEYBOARD)

    elif state == "waiting_for_delete_event":
        stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)

        if text.lower() == 'да':

            try:
                selected_event = stage_service.get_event(str(update.message.from_user.id))

                event_service.delete(str(update.message.from_user.id), selected_event)
                stage_service.change_event(str(update.message.from_user.id), None)

                stage_service.change_window(str(update.message.from_user.id), WindowType.MAIN_KEYBOARD)
                await update.message.reply_text("Успешно удалилось", reply_markup=MAIN_KEYBOARD)
            except Exception as e:
                await update.message.reply_text(f"{e}", reply_markup=CHOOSE_KEYBOARD)
        else:
            await update.message.reply_text("Вы решили не удалять", reply_markup=CHOOSE_KEYBOARD)


    elif state == "waiting_for_delete_notice_number":
        selected_event = stage_service.get_event(str(update.message.from_user.id))
        notices = notice_service.get_all(selected_event)
        if text.isdigit() and len(notices) >= int(text) > 0:
            selected_notice = notices[int(text) - 1]
            stage_service.change_notice(str(update.message.from_user.id), selected_notice.notice_id)

            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DELETE_NOTICE)
            stage_service.change_window(str(update.message.from_user.id), WindowType.CHOOSE_KEYBOARD)

            await update.message.reply_text(
                f"Вы выбрали напоминание:\n"
                f"Дата: {selected_notice.date}\n"
                f"Время: {str(selected_notice.time)[:5]}\n\n"
                f"Вы уверены что хотите его удалить? Да/Нет",
                reply_markup=CANCEL_KEYBOARD
            )
        else:
            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_DELETE_NOTICE_NUMBER)

            await update.message.reply_text("Введите номер вашего напоминания или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_delete_notice":
        stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)
        stage_service.change_window(str(update.message.from_user.id), WindowType.CHOOSE_KEYBOARD)

        stage_service.change_notice(str(update.message.from_user.id), None)

        if text.lower() == 'да':
            try:
                selected_notice = stage_service.get_notice(str(update.message.from_user.id))
                selected_event = stage_service.get_event(str(update.message.from_user.id))
                notice_service.delete(selected_notice,
                                      selected_event)

                await update.message.reply_text("Успешно удалилось.", reply_markup=CHOOSE_KEYBOARD)
            except Exception as e:
                await update.message.reply_text(f"{e}", reply_markup=CHOOSE_KEYBOARD)
        else:
            await update.message.reply_text("Вы решили не удалять.", reply_markup=CHOOSE_KEYBOARD)

    elif state == "waiting_for_event":
        events = event_service.get_all(str(update.message.from_user.id))
        if text.isdigit() and len(events) >= int(text) > 0:
            selected_event = events[int(text) - 1]

            stage_service.change_event(str(update.message.from_user.id), selected_event.event_id)

            stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)
            stage_service.change_window(str(update.message.from_user.id), WindowType.CHOOSE_KEYBOARD)

            await update.message.reply_text(
                f"Вы выбрали\n```событие:\n"
                f"Дата: {selected_event.date}\n"
                f"Время: {str(selected_event.time)[:5]}\n"
                f"Название: {selected_event.name}\n"
                f"Описание: {selected_event.description}\n```",
                reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown'
            )
        else:
            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_EVENT)

            await update.message.reply_text("Введите номер вашего события или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_date_notice_choose":
        if is_valid_date(text):
            context.user_data["date"] = text
            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_TIME_NOTICE_CHOOSE)

            await update.message.reply_text("Введите время напоминания (в формате ЧЧ:ММ) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)
        else:
            await update.message.reply_text("Введите дату напоминания (в формате ГГГГ-ММ-ДД) или нажмите 'Отмена':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_time_notice_choose":
        if is_valid_time(context.user_data['date'], text):
            try:
                context.user_data["time"] = text
                stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)
                selected_event = stage_service.get_event(str(update.message.from_user.id))

                notice_id = notice_service.add(
                    noticeDTO.AddNoticeRequest(selected_event,
                                               datetime.strptime(
                                                   context.user_data['date'],
                                                   "%Y-%m-%d").date(),
                                               datetime.strptime(
                                                   context.user_data['time'],
                                                   "%H:%M").time()
                                               ))
                notice = notice_service.get(notice_id)

                notice_time = datetime.combine(notice.date, notice.time)
                my_time_zone = 3
                user_time_zone = user_service.get_time_zone(str(update.message.from_user.id))
                time_zone_difference = user_time_zone - my_time_zone

                delay = (notice_time - datetime.now()).total_seconds() - (time_zone_difference * 3600)

                def time_until_event(event: eventModel.Event, notice: noticeModel.Notice) -> dict:
                    event_datetime = datetime.combine(event.date, event.time)
                    notice_datetime = datetime.combine(notice.date, notice.time)

                    delta = event_datetime - notice_datetime

                    days = delta.days
                    hours, remainder = divmod(delta.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)

                    return {
                        "d": days,
                        "h": hours,
                        "m": minutes
                    }

                def time_until_event(event: eventModel.Event, notice: noticeModel.Notice) -> dict:
                    event_datetime = datetime.combine(event.date, event.time)
                    notice_datetime = datetime.combine(notice.date, notice.time)

                    delta = event_datetime - notice_datetime

                    days = delta.days
                    hours, remainder = divmod(delta.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)

                    return {
                        "дни": days,
                        "часы": hours,
                        "минуты": minutes
                    }

                async def send_reminder(context: CallbackContext):
                    notice_reminder = context.job.data
                    event = event_service.get(notice.event_id, str(update.effective_chat.id))
                    until = time_until_event(event, notice)
                    if notice_service.check_exist(notice.notice_id):
                        remind = (f"🔔 Напоминание!\n"
                                  f"```Событие:\n"
                                  f"Название: {event.name}\n"
                                  f"Описание: {event.description}\n"
                                  f"Дата: {event.date}\n"
                                  f"Время: {str(event.time)[:5]}\n"
                                  f"```\n\n"
                                  f"Наступит через *{until.get('d')} дней {until.get('h')}:{until.get('m')}*")

                        await context.bot.send_message(chat_id=update.effective_chat.id, text=remind,
                                                       parse_mode='Markdown')
                        notice_service.delete(notice.notice_id, event.event_id)

                context.job_queue.run_once(send_reminder, delay, data=(notice))  # data=(notice_id,

                await update.message.reply_text("Напоминание успешно добавлено", reply_markup=CHOOSE_KEYBOARD)
            except Exception as e:
                await update.message.reply_text(f"Ошибка: {e}", reply_markup=CHOOSE_KEYBOARD)
        else:
            await update.message.reply_text("Введите время напоминания (в формате ЧЧ:ММ) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_fix_date":
        if is_valid_date(text):
            context.user_data["fix_date"] = text
            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_FIX_TIME)

            await update.message.reply_text("Введите новое время события (в формате ЧЧ:ММ) или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)
        else:
            await update.message.reply_text("Введите новую дату события (в формате ГГГГ-ММ-ДД) или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)

    elif state == "waiting_for_fix_time":
        if is_valid_time(context.user_data['fix_date'], text):
            context.user_data["fix_time"] = text
            stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_FIX_NAME)

            await update.message.reply_text("Введите новое название события или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)
        else:
            await update.message.reply_text("Введите новое время события (в формате ЧЧ:ММ) или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)

    elif state == "waiting_for_fix_name":
        context.user_data["fix_name"] = text
        stage_service.change_stage(str(update.message.from_user.id), StageType.WAITING_FOR_FIX_DESCRIPTION)

        await update.message.reply_text("Введите новое описание события или нажмите 'Назад':",
                                        reply_markup=FIX_KEYBOARD)

    elif state == "waiting_for_fix_description":
        context.user_data["fix_description"] = text
        try:
            stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)

            fix_date = datetime.strptime(context.user_data['fix_date'], "%Y-%m-%d").date() \
                if context.user_data['fix_date'] is not None else None
            fix_time = datetime.strptime(context.user_data['fix_time'], "%H:%M").time() \
                if context.user_data['fix_time'] is not None else None

            selected_event = stage_service.get_event(str(update.message.from_user.id))
            event_service.change(eventDTO.ChangeEventRequest(str(update.message.from_user.id),
                                                             selected_event,
                                                             fix_date, fix_time,
                                                             context.user_data['fix_name'],
                                                             context.user_data['fix_description']
                                                             ))
            await update.message.reply_text("Событие было изменено", reply_markup=CHOOSE_KEYBOARD)
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}", reply_markup=CHOOSE_KEYBOARD)

    elif state == "waiting_for_time_zone":
        if is_valid_time_zone(text):
            user_service.change_time_zone(str(update.message.from_user.id), int(text))
            stage_service.change_stage(str(update.message.from_user.id), StageType.NONE)

            await update.message.reply_text("Часовой пояс установлен",
                                            reply_markup=MAIN_KEYBOARD)
        else:
            await update.message.reply_text("Введите ваш часовой пояс (+/- <число>):")

    else:
        previous_menu = stage_service.get_window(str(update.message.from_user.id))

        await update.message.reply_text(f"Неизвестная команда", reply_markup=previous_menu.value)

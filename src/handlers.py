import repository.connector.PGConnector as Connector
import service.implementation.Event as eventService
import repository.implementation.Event as eventStorage
import service.implementation.Notice as noticeService
import repository.implementation.Notice as noticeStorage
import service.implementation.User as userService
import repository.implementation.User as userStorage
from datetime import datetime
import re

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters, JobQueue

import asyncio
import dto.event as eventDTO
import model.event as eventModel
import dto.notice as noticeDTO
import model.notice as noticeModel

connector = Connector.PostgresDBConnector()

event_repository = eventStorage.EventRepository(connector)
event_service = eventService.EventService(connector, event_repository)

notice_repository = noticeStorage.NoticeRepository(connector)
notice_service = noticeService.NoticeService(connector, notice_repository)

user_repository = userStorage.UserRepository(connector)
user_service = userService.UserService(connector, user_repository)

MAIN_KEYBOARD = ReplyKeyboardMarkup([["Get", "Add"], ["Info", "Choose", "Delete"]], resize_keyboard=True)
BACK_KEYBOARD = ReplyKeyboardMarkup([["Back"]], resize_keyboard=True, one_time_keyboard=True)
CHOOSE_KEYBOARD = ReplyKeyboardMarkup([["Get", "Fix"], ["Info", "Delete event"], ["Add", "Delete notice"], ["Back"]],
                                      resize_keyboard=True)
CANCEL_KEYBOARD = ReplyKeyboardMarkup([["Cancel"]], resize_keyboard=True, one_time_keyboard=True)
FIX_KEYBOARD = ReplyKeyboardMarkup([["Cancel", "Next"]], resize_keyboard=True, one_time_keyboard=True)


def is_valid_date(date_str: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
        return False

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date_obj >= datetime.today().date()
    except ValueError:
        return False


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


async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [["Старт"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Нажмите 'Старт' для продолжения:", reply_markup=reply_markup)


def get_menu(menu_name: str):
    if menu_name == "main":
        return MAIN_KEYBOARD
    elif menu_name == "choose":
        return CHOOSE_KEYBOARD
    else:
        return MAIN_KEYBOARD


async def show_main_menu(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = "main"

    chat_id = update.message.chat.id
    tg_id = update.message.from_user.id
    print('try to add')
    try:
        user_service.add(str(tg_id), str(chat_id))
    except Exception as e:
        print(e)

    await update.message.reply_text("Выберите действие:", reply_markup=MAIN_KEYBOARD)


async def back_to_main_menu(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = "main"
    await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=MAIN_KEYBOARD)


async def next_to_fix_event(update: Update, context: CallbackContext) -> None:
    state = context.user_data.get("state", None)
    if state == 'waiting_for_fix_date':
        context.user_data["fix_date"] = None
        context.user_data["state"] = 'waiting_for_fix_time'
        await update.message.reply_text(
            "Вы пропустили изменение даты.\n\nВведите новое время события или нажмите 'Назад':",
            reply_markup=FIX_KEYBOARD)
    elif state == 'waiting_for_fix_time':
        context.user_data["fix_time"] = None
        context.user_data["state"] = 'waiting_for_fix_name'
        await update.message.reply_text(
            "Вы пропустили изменение времени.\n\nВведите новое название события или нажмите 'Назад':",
            reply_markup=FIX_KEYBOARD)
    elif state == 'waiting_for_fix_name':
        context.user_data["fix_name"] = None
        context.user_data["state"] = 'waiting_for_fix_description'
        await update.message.reply_text(
            "Вы пропустили изменение названия.\n\nВведите новое описание события или нажмите 'Назад':",
            reply_markup=FIX_KEYBOARD)
    elif state == 'waiting_for_fix_description':
        try:
            context.user_data.pop("state", None)
            fix_date = datetime.strptime(context.user_data['fix_date'], "%Y-%m-%d").date() \
                if context.user_data['fix_date'] is not None else None
            fix_time = datetime.strptime(context.user_data['fix_time'], "%H:%M").time() \
                if context.user_data['fix_time'] is not None else None
            event_service.change(eventDTO.ChangeEventRequest(str(update.message.from_user.id),
                                                             context.user_data.get("selected_event").event_id,
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
    text = update.message.text
    menu = context.user_data.get("menu", "main")  # Получаем текущее меню

    if menu == "main":
        if text == "Get":
            await get_all_event(update, context)
            return
        elif text == "Add":
            await update.message.reply_text(f"Было выбрано: '{text}'", reply_markup=CANCEL_KEYBOARD)
            await add_data(update, context)
            return
        elif text == "Info":
            await get_info(update, context)
            return
        elif text == "Delete":
            await update.message.reply_text(f"Было выбрано: '{text}'", reply_markup=CANCEL_KEYBOARD)
            await delete_all_data(update, context)
            return
        elif text == "Choose":
            await update.message.reply_text(f"Было выбрано: '{text}'", reply_markup=CANCEL_KEYBOARD)
            await choose_event(update, context)
            return
        await update.message.reply_text("Обработка завершена. Возвращаюсь в главное меню.", reply_markup=MAIN_KEYBOARD)

    elif menu == "choose":
        if text == "Get":
            await get_all_notice(update, context)
            return
        elif text == "Info":
            await get_info(update, context)
            return
        elif text == "Delete event":
            await update.message.reply_text(f"Было выбрано: '{text}'", reply_markup=CANCEL_KEYBOARD)
            await delete_event(update, context)
            return
        elif text == "Delete notice":
            await update.message.reply_text(f"Было выбрано: '{text}'", reply_markup=CANCEL_KEYBOARD)
            await delete_notice(update, context)
            return
        elif text == "Add":
            await update.message.reply_text(f"Было выбрано: '{text}'", reply_markup=CANCEL_KEYBOARD)
            await add_notice(update, context)
            return
        await update.message.reply_text("Обработка завершена. Возвращаюсь в меню Choose.", reply_markup=CHOOSE_KEYBOARD)


async def handle_cancel(update: Update, context: CallbackContext) -> None:
    state = context.user_data.get("state", None)
    previous_menu = context.user_data.get("menu", "main")
    # if state == "waiting_for_date":
    #     await update.message.reply_text("Добавление события отменено. Возвращаюсь в главное меню.",
    #                                     reply_markup=MAIN_KEYBOARD)
    # elif state == "waiting_for_time":
    #     await update.message.reply_text("Ввод времени отменен. Введите дату снова или вернитесь в меню.",
    #                                     reply_markup=CANCEL_KEYBOARD)
    #     context.user_data["state"] = "waiting_for_date"
    #     return
    # elif state == "waiting_for_name":
    #     await update.message.reply_text("Ввод названия отменен. Введите время снова или вернитесь в меню.",
    #                                     reply_markup=CANCEL_KEYBOARD)
    #     context.user_data["state"] = "waiting_for_time"
    #     return
    # elif state == "waiting_for_description":
    #     await update.message.reply_text("Ввод описания отменен. Введите название снова или вернитесь в меню.",
    #                                     reply_markup=CANCEL_KEYBOARD)
    #     context.user_data["state"] = "waiting_for_name"
    #     return
    if state == "back":
        context.user_data.pop("state", None)
        await update.message.reply_text("Вы вернулись в предыдущее меню.", reply_markup=get_menu(previous_menu))
        return

    context.user_data.pop("state", None)
    await update.message.reply_text("Вы вернулись в предыдущее меню.", reply_markup=get_menu(previous_menu))


async def add_data(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "main")
    context.user_data["state"] = "waiting_for_date"
    await update.message.reply_text("Введите дату события (в формате YYYY-MM-DD) или нажмите 'Отмена':",
                                    reply_markup=CANCEL_KEYBOARD)


async def get_all_event(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "main")
    events = event_service.get_all(str(update.message.from_user.id))

    if not events:
        await update.message.reply_text("У вас нет событий.", reply_markup=MAIN_KEYBOARD)
        return

    events_text = "Список ваших событий:\n\n"

    for i, event in enumerate(events, start=1):
        events_text += (f"```Событие_#{i}\n"
                        f"Дата: {event.date}\n"
                        f"Время: {str(event.time)[:5]}\n"
                        f"Уведомлений: {10 - event.notice_count}\n"
                        f"Название: {event.name}\n"
                        f"Описание: {event.description}\n"
                        f"```\n")

    await update.message.reply_text(events_text, reply_markup=MAIN_KEYBOARD, parse_mode='Markdown')


async def get_info(update: Update, context: CallbackContext) -> None:
    previous_menu = context.user_data.get("menu", "main")

    text_info = (f"*Информация*\n"
                 f"я бот долбаеб")

    await update.message.reply_text(text_info, reply_markup=get_menu(previous_menu), parse_mode='Markdown')


async def choose_event(update: Update, context: CallbackContext) -> None:
    """Начало процесса добавления данных (запрос даты)."""
    context.user_data["menu"] = context.user_data.get("menu", "main")
    context.user_data["state"] = "waiting_for_event"
    await update.message.reply_text("Введите номер событие или нажмите 'Отмена':",
                                    reply_markup=CANCEL_KEYBOARD)


async def get_all_notice(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "choose")

    selected_event = event_service.get(context.user_data.get("selected_event").event_id,
                                       str(update.message.from_user.id))

    notices = notice_service.get_all(selected_event.event_id)

    if not notices:
        await update.message.reply_text("У вас нет уведомлений для данного события.", reply_markup=CHOOSE_KEYBOARD)
        return

    events_text = (f"```Событие\n"
                   f"Дата: {selected_event.date}\n"
                   f"Время: {str(selected_event.time)[:5]}\n"
                   f"Уведомлений: {10 - selected_event.notice_count}\n"
                   f"Название: {selected_event.name}\n"
                   f"Описание: {selected_event.description}\n"
                   f"```\n")

    events_text += "Список уведомлений:\n\n"

    for i, notice in enumerate(notices, start=1):
        events_text += (f"```Уведомление_#{i}\n"
                        f"Дата: {notice.date}\n"
                        f"Время: {str(notice.time)[:5]}\n"
                        f"```\n")

    await update.message.reply_text(events_text, reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown')


async def delete_all_data(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "main")  # Запоминаем, из какого меню вызвано
    context.user_data["state"] = "waiting_for_delete_all"
    await update.message.reply_text("Вы уверены что хотите удалить все события? Да/Нет",
                                    reply_markup=CANCEL_KEYBOARD)


async def delete_event(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "choose")
    context.user_data["state"] = "waiting_for_delete_event"
    await update.message.reply_text("Вы уверены что хотите удалить данное события? Да/Нет",
                                    reply_markup=CANCEL_KEYBOARD)


async def delete_notice(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "choose")
    context.user_data["state"] = "waiting_for_delete_notice_number"
    await update.message.reply_text("Введите номер напоминания для удаления",
                                    reply_markup=CANCEL_KEYBOARD)


async def add_notice(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "choose")
    context.user_data["state"] = "waiting_for_date_notice_choose"
    await update.message.reply_text("Введите дату напоминания (в формате YYYY-MM-DD) или нажмите 'Отмена':",
                                    reply_markup=CANCEL_KEYBOARD)


async def fix_event(update: Update, context: CallbackContext) -> None:
    context.user_data["menu"] = context.user_data.get("menu", "choose")
    context.user_data["state"] = "waiting_for_fix_date"
    await update.message.reply_text("Введите новую дату события (в формате YYYY-MM-DD) или нажмите 'Отмена':",
                                    reply_markup=FIX_KEYBOARD)


async def handle_user_input(update: Update, context: CallbackContext) -> None:
    state = context.user_data.get("state", None)
    text = update.message.text

    if state == "waiting_for_date":
        if is_valid_date(text):
            context.user_data["date"] = text
            context.user_data["state"] = "waiting_for_time"
            await update.message.reply_text("Введите время события (в формате HH:MM) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)
        else:
            await update.message.reply_text("Введите дату события (в формате YYYY-MM-DD) или нажмите 'Отмена':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_time":
        if is_valid_time(context.user_data['date'], text):
            context.user_data["time"] = text
            context.user_data["state"] = "waiting_for_name"
            await update.message.reply_text("Введите название события или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)
        else:
            await update.message.reply_text("Введите время события (в формате HH:MM) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_name":
        context.user_data["name"] = text
        context.user_data["state"] = "waiting_for_description"
        await update.message.reply_text("Введите описание события или нажмите 'Назад':", reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_description":
        context.user_data["description"] = text
        context.user_data["event_id"] = event_service.add(eventDTO.AddEventRequest(str(update.message.from_user.id),
                                                                                   datetime.strptime(
                                                                                       context.user_data['date'],
                                                                                       "%Y-%m-%d").date(),
                                                                                   datetime.strptime(
                                                                                       context.user_data['time'],
                                                                                       "%H:%M").time(),
                                                                                   context.user_data['name'],
                                                                                   context.user_data['description']))

        context.user_data["state"] = "waiting_for_date_notice"
        await update.message.reply_text("Событие было успешно создано\nВведите дату напоминания или нажмите 'Назад':",
                                        reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_date_notice":
        if is_valid_date(text):
            context.user_data["date_notice"] = text
            context.user_data["state"] = "waiting_for_time_notice"
            await update.message.reply_text("Введите время напоминания или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)
        else:
            await update.message.reply_text("Введите дату напоминания (в формате YYYY-MM-DD) или нажмите 'Отмена':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_time_notice":
        if is_valid_time(context.user_data['date_notice'], text):
            context.user_data["time_notice"] = text
            context.user_data["state"] = "waiting_for_date_notice"

            notice_service.add(noticeDTO.AddNoticeRequest(context.user_data.get("selected_event").event_id,
                                                          datetime.strptime(
                                                              context.user_data['date_notice'],
                                                              "%Y-%m-%d").date(),
                                                          datetime.strptime(
                                                              context.user_data['time_notice'],
                                                              "%H:%M").time()))

            await update.message.reply_text("Введите дату следующего напоминания или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

            await update.message.reply_text(
                f"Событие добавлено:\nДата: {context.user_data['date']}\nВремя: {context.user_data['time']}\nНазвание: {context.user_data['name']}\nОписание: {context.user_data['description']}",
                reply_markup=MAIN_KEYBOARD)
        else:
            await update.message.reply_text("Введите время напоминания (в формате HH:MM) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_delete_all":
        if text.lower() == 'да':
            context.user_data["state"] = "back"
            try:
                event_service.delete_all(str(update.message.from_user.id))
                await update.message.reply_text("Успешно удалилось.", reply_markup=MAIN_KEYBOARD)
            except Exception as e:
                await update.message.reply_text(f"{e}", reply_markup=MAIN_KEYBOARD)
        elif text.lower() == 'нет':
            await update.message.reply_text("Вы решили не удалять.", reply_markup=MAIN_KEYBOARD)
        else:
            context.user_data["state"] = "waiting_for_delete_all"
            await update.message.reply_text("Введите Да/Нет или нажмите 'Назад':", reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_delete_event":
        if text.lower() == 'да':
            # context.user_data["state"] = "back"
            context.user_data.pop("state", None)

            try:
                event_service.delete(str(update.message.from_user.id), context.user_data.get("selected_event").event_id)
                context.user_data.pop("selected_event", None)
                context.user_data["menu"] = "main"
                await update.message.reply_text("Успешно удалилось.", reply_markup=MAIN_KEYBOARD)
            except Exception as e:
                await update.message.reply_text(f"{e}", reply_markup=CHOOSE_KEYBOARD)
        elif text.lower() == 'нет':
            await update.message.reply_text("Вы решили не удалять.", reply_markup=CHOOSE_KEYBOARD)
        else:
            context.user_data["state"] = "waiting_for_delete_event"
            await update.message.reply_text("Введите Да/Нет или нажмите 'Назад':", reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_delete_notice_number":
        notices = notice_service.get_all(context.user_data.get("selected_event").event_id)
        if text.isdigit() and len(notices) >= int(text) > 0:
            selected_notice = notices[int(text) - 1]
            print(selected_notice)
            context.user_data["selected_notice"] = selected_notice
            context.user_data["state"] = "waiting_for_delete_notice"
            context.user_data["menu"] = "choose"
            await update.message.reply_text(
                f"Вы выбрали напоминание:\n"
                f"Дата: {selected_notice.date}\n"
                f"Время: {selected_notice.time}\n\n"
                f"Вы уверены что хотите его удалить? Да/Нет",
                reply_markup=CANCEL_KEYBOARD
            )
        else:
            context.user_data["state"] = "waiting_for_delete_notice_number"
            await update.message.reply_text("Введите номер вашего напоминания или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_delete_notice":
        if text.lower() == 'да':
            try:
                notice_service.delete(context.user_data.get("selected_notice").notice_id,
                                      context.user_data.get("selected_event").event_id)
                context.user_data.pop("selected_notice", None)
                context.user_data.pop("state", None)
                context.user_data["menu"] = "choose"
                await update.message.reply_text("Успешно удалилось.", reply_markup=CHOOSE_KEYBOARD)
            except Exception as e:
                await update.message.reply_text(f"{e}", reply_markup=CHOOSE_KEYBOARD)
        elif text.lower() == 'нет':
            await update.message.reply_text("Вы решили не удалять.", reply_markup=CHOOSE_KEYBOARD)
        else:
            context.user_data["state"] = "waiting_for_delete_notice"
            await update.message.reply_text("Введите Да/Нет или нажмите 'Назад':", reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_event":
        events = event_service.get_all(str(update.message.from_user.id))
        if text.isdigit() and len(events) >= int(text) > 0:
            selected_event = events[int(text) - 1]

            context.user_data["selected_event"] = selected_event
            context.user_data["state"] = None
            context.user_data["menu"] = "choose"
            await update.message.reply_text(
                f"Вы выбрали\n```событие:\n"
                f"Дата: {selected_event.date}\n"
                f"Время: {selected_event.time}\n"
                f"Название: {selected_event.name}\n"
                f"Описание: {selected_event.description}\n```",
                reply_markup=CHOOSE_KEYBOARD, parse_mode='Markdown'
            )
        else:
            context.user_data["state"] = "waiting_for_event"
            await update.message.reply_text("Введите номер вашего события или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_date_notice_choose":
        if is_valid_date(text):
            context.user_data["date"] = text
            context.user_data["state"] = "waiting_for_time_notice_choose"
            await update.message.reply_text("Введите время напоминания (в формате HH:MM) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)
        else:
            await update.message.reply_text("Введите дату напоминания (в формате YYYY-MM-DD) или нажмите 'Отмена':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_time_notice_choose":
        if is_valid_time(context.user_data['date'], text):
            try:
                context.user_data["time"] = text
                context.user_data.pop("state", None)
                notice_id = notice_service.add(
                    noticeDTO.AddNoticeRequest(context.user_data.get("selected_event").event_id,
                                               datetime.strptime(
                                                   context.user_data['date'],
                                                   "%Y-%m-%d").date(),
                                               datetime.strptime(
                                                   context.user_data['time'],
                                                   "%H:%M").time()
                                               ))
                print(notice_id)
                notice = notice_service.get(notice_id)
                print(notice)
                print('start create reminder')

                notice_time = datetime.combine(notice.date, notice.time)

                delay = (notice_time - datetime.now()).total_seconds()

                async def send_reminder(context: CallbackContext):
                    notice_reminder = context.job.data
                    print(notice)
                    print(notice_reminder)
                    event = event_service.get(notice.event_id, str(update.effective_chat.id))

                    if notice_service.check_exist(notice.notice_id):
                        remind = (f"🔔 Напоминание!\n"
                                f"```Событие:\n"
                                f"Название: {event.name}\n"
                                f"Описание: {event.description}\n"
                                f"Дата: {event.date}\n"
                                f"Время: {str(event.time)[:5]}\n"
                                f"```\n\n"
                                f"Наступит через *{time_until_event(event, notice)}*")
                        await context.bot.send_message(chat_id=update.effective_chat.id, text=remind,
                                                       parse_mode='Markdown')
                        notice_service.delete(notice.notice_id, event.event_id)

                    # await context.bot.send_message(
                    #     chat_id=update.effective_chat.id,
                    #     text="Это ваше напоминание!",
                    #     reply_markup=CHOOSE_KEYBOARD
                    # )

                # Добавляем задачу в очередь с задержкой
                context.job_queue.run_once(send_reminder, delay, data=(notice))  # data=(notice_id,
                #     context.user_data.get("selected_event").event_id))

                await update.message.reply_text("Напоминание успешно добавлено", reply_markup=CHOOSE_KEYBOARD)
                # await add_reminder(context, str(update.message.from_user.id),
                #                    context.user_data.get("selected_event"), notice)
            except Exception as e:
                await update.message.reply_text(f"Ошибка: {e}", reply_markup=CHOOSE_KEYBOARD)
        else:
            await update.message.reply_text("Введите время напоминания (в формате HH:MM) или нажмите 'Назад':",
                                            reply_markup=CANCEL_KEYBOARD)

    elif state == "waiting_for_fix_date":
        if is_valid_date(text):
            context.user_data["fix_date"] = text
            context.user_data["state"] = "waiting_for_fix_time"
            await update.message.reply_text("Введите новое время события или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)
        else:
            await update.message.reply_text("Введите новую дату события в формате или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)

    elif state == "waiting_for_fix_time":
        if is_valid_time(context.user_data['fix_date'], text):
            context.user_data["fix_time"] = text
            context.user_data["state"] = "waiting_for_fix_name"
            await update.message.reply_text("Введите новое название события или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)
        else:
            await update.message.reply_text("Введите новое время события в формате или нажмите 'Назад':",
                                            reply_markup=FIX_KEYBOARD)

    elif state == "waiting_for_fix_name":
        context.user_data["fix_name"] = text
        context.user_data["state"] = "waiting_for_fix_description"
        await update.message.reply_text("Введите новое описание события или нажмите 'Назад':",
                                        reply_markup=FIX_KEYBOARD)

    elif state == "waiting_for_fix_description":
        context.user_data["fix_description"] = text
        try:
            context.user_data.pop("state", None)
            fix_date = datetime.strptime(context.user_data['fix_date'], "%Y-%m-%d").date() \
                if context.user_data['fix_date'] is not None else None
            fix_time = datetime.strptime(context.user_data['fix_time'], "%H:%M").time() \
                if context.user_data['fix_time'] is not None else None
            event_service.change(eventDTO.ChangeEventRequest(str(update.message.from_user.id),
                                                             context.user_data.get("selected_event").event_id,
                                                             fix_date, fix_time,
                                                             context.user_data['fix_name'],
                                                             context.user_data['fix_description']
                                                             ))
            await update.message.reply_text("Событие было изменено", reply_markup=CHOOSE_KEYBOARD)
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}", reply_markup=CHOOSE_KEYBOARD)

    else:
        previous_menu = context.user_data.get("menu", "main")
        await update.message.reply_text(f"Неизвестная команда", reply_markup=get_menu(previous_menu))


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

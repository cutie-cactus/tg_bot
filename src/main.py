from handlers import *
from dotenv import load_dotenv
import os


def main():
    """@main
    @brief Точка входа телеграм-бота
    @details Реализует настройку и запуск бота с обработчиками команд и сообщений
    
    @var dotenv_path - Путь к файлу конфигурации
    @var token - Токен бота из переменных окружения
    @var app - Экземпляр телеграм-приложения
    
    @throws FileNotFoundError если отсутствует config/config.env
    @throws KeyError если отсутствует TELEGRAM_BOT_TOKEN
    """
    load_dotenv(dotenv_path="config/config.env")
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    app = Application.builder().token(token).build()

    # Основные обработчики действий
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^Старт$"), show_main_menu))

    """@handlers
    @brief Группа обработчиков для основных операций
    @details Реагируют на текстовые команды:
    @var Get - Получение информации
    @var Add - Добавление данных
    @var Info - Информация
    @var Fix - Исправление
    @var Delete - Удаление
    @var Choose - Выбор элемента
    @var Delete event - Удаление события
    @var Delete notice - Удаление уведомления
    """
    app.add_handler(MessageHandler(filters.Regex(r"^(Get|Add|Info|Fix|Delete|Choose|Delete\sevent|Delete\snotice)$"),
                                   handle_actions))

    # Вспомогательные обработчики
    app.add_handler(MessageHandler(filters.Regex("^Cancel$"), handle_cancel))
    app.add_handler(MessageHandler(filters.Regex("^Back$"), back_to_main_menu))
    app.add_handler(MessageHandler(filters.Regex("^Next$"), next_to_fix_event))

    """@handler
    @brief Универсальный обработчик текстового ввода
    @details Перехватывает любой текст без команд:
    @var filters.TEXT - Фильтр текстовых сообщений
    @var ~filters.COMMAND - Исключает сообщения с командами
    """
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))

    """@method
    @brief Запуск бота в режиме polling
    @details Бесконечный цикл проверки обновлений через API Telegram
    """
    app.run_polling()


if __name__ == "__main__":
    main()

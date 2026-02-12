from handlers import *
from dotenv import load_dotenv
import os


def main():
    load_dotenv(dotenv_path="config/config.env")
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    app = Application.builder() \
        .token(token) \
        .get_updates_read_timeout(60) \
        .get_updates_write_timeout(60) \
        .get_updates_connect_timeout(60) \
        .get_updates_pool_timeout(60) \
        .build()

    # app = Application.builder().token(token).build()
    

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^Старт$"), show_main_menu))

    app.add_handler(MessageHandler(filters.Regex(r"^(Get|Add|Info|Fix|Delete|Choose|Delete\sevent|Delete\snotice)$"),
                                   handle_actions))

    app.add_handler(MessageHandler(filters.Regex("^Cancel$"), handle_cancel))
    app.add_handler(MessageHandler(filters.Regex("^Back$"), back_to_main_menu))
    app.add_handler(MessageHandler(filters.Regex("^Next$"), next_to_fix_event))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_input))

    app.run_polling()


if __name__ == "__main__":
    main()

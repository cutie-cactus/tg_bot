from handlers import *

TOKEN = "8115091162:AAFjgA3BJDCyzrsgKFc0RPRj8M4vfdwp1QY"


def main():
    app = Application.builder().token(TOKEN).build()

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

import os
import pickle
import weather_pars
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
storage = []


def start(update, context):
    """Send a message when the command /start is issued."""

    update.message.reply_text('Hi! Input correctly date, for example-  25 июля ')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    message = None
    # update.message.reply_text(update.message.text)
    user_text = update.message.text
    weather_data = weather_pars.get_weather()

    for item in weather_data:
        if item['date'] == user_text:
            message = item['date'] + '\n' + item['morning'] + '\n' + item['day_time'] + '\n' + item['evening'] + '\n' + \
                      item['night'] + '\n' + item['wind'] + '\n' + item['pressure']
            update.message.reply_text(message)
    else:
        update.message.reply_text("If you can't see weather, input more correct and try again.")


def main():
    token = os.getenv("TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

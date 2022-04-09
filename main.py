import logging
import os
import threading

from telegram.ext import *

import app
from updater import Updater as NewsUpdater
from news import *

newsUpdater: NewsUpdater

started = False

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

users: set = set()


PORT = int(os.environ.get('PORT', 5000))
TOKEN = '5078454106:AAF3BB8mc_FFAxTNxPH3obrw0gLfBwngMXY'

def startHandler(update, context: CallbackContext):
    update.message.reply_text(f'Hello {update.message.chat.first_name}, I am economic_news_bot.')
    helpHandler(update, context)

    users.add(update.message)


def helpHandler(update, context):
    update.message.reply_text('I can show you some news, just type /news')


def newsHandler(update, context):
    global newsUpdater

    for news in newsUpdater.news.news:
        update.message.reply_text(str(news))


def loadNewsHandler(update, context):
    global newsUpdater

    update.message.reply_text("Loading")
    newsUpdater.news.load()
    update.message.reply_text("Loading end")


def echoHandler(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def onUpdate(updated_news: list[News]):
    for news in updated_news:
        for user in users:
            user.reply_text(str(news))


def main():
    global newsUpdater
    newsUpdater = NewsUpdater(onUpdate)
    newsUpdater.start()

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", startHandler))
    dp.add_handler(CommandHandler("help", helpHandler))
    dp.add_handler(CommandHandler("news", newsHandler))
    dp.add_handler(MessageHandler(Filters.text, echoHandler))

    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://economy-bot-python.herokuapp.com/" + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()

import os

from flask import Flask, request

import telebot

from updater import Updater as NewsUpdater
from news import *


newsUpdater: NewsUpdater

users: set = set()

PORT = int(os.environ.get('PORT', 5000))
TOKEN = '5078454106:AAH11W5rIlCui7eH_QD0Omz05QKNbvI3dhM'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

isStarted = False

@bot.message_handler(commands=['start'])
def startHandler(message):
    bot.reply_to(message, f'Hello {message.from_user.first_name}, I am Economic Bot.')
    helpHandler(message)

@bot.message_handler(commands=['subscribe'])
def subscribeHandler(message):
    bot.reply_to(message, "You successfully subscribed to news\nTo unsubscribe type /unsubscribe")
    users.add(message)

@bot.message_handler(commands=['unsubscribe'])
def unsubscribeHandler(message):
    users.remove(message)

@bot.message_handler(commands=['help'])
def helpHandler(message):
    bot.reply_to(message, 'I can show you some news, just type /news\nYou can subscribe to news just type /subscribe')

@bot.message_handler(commands=['news'])
def newsHandler(message):
    global newsUpdater

    for news in newsUpdater.news.news:
        bot.reply_to(message, str(news))


def onUpdate(updated_news: list[News]):
    for news in updated_news:
        for user in users:
            bot.reply_to(user, str(news))

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    global isStarted
    if isStarted:
        return 'Bot already started', 200

    bot.remove_webhook()
    bot.set_webhook(url='https://economy-bot-python.herokuapp.com/' + TOKEN)

    global newsUpdater
    newsUpdater = NewsUpdater(onUpdate)
    newsUpdater.start()

    isStarted = True

    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

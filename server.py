def setup(updater, token, port):
    updater.start_webhook(listen="0.0.0.0", port=int(port), url_path=token)
    updater.bot.setWebhook('https://economy-bot-python.herokuapp.com/' + token)
    updater.idle()

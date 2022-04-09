import os

from flask import Flask

app = Flask(__name__)


@app.route('/')
def homepage():
    os.execl(os.dirname(__file__) + '/shutdown.py', '--')
    return "Bot is running"


def setup():
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=os.environ.get("PORT", 5000))
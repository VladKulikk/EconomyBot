import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def setup():
    port: int = int(os.environ.get('PORT', 5000))

    print("Setup on port ", port)
    app.run(threaded=True, port=port)

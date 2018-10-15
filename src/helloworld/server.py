import platform

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world from Python {}!".format(platform.python_version())


@app.route("/status")
def status():
    return "OK"


if __name__ == "__main__":
    # setting the host to 0.0.0.0 allows us to access from outside a sandbox
    app.run(host="0.0.0.0", port=8080)
